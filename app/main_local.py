from fastapi import FastAPI, Depends, UploadFile, File
from pydantic import BaseModel
from torchvision import transforms
from torchvision.models import ResNet
from PIL import Image
import io
import torch
import torch.nn.functional as F
import wandb
import os

MODELS_DIR = "models"
MODEL_FILE_NAME = "model.pth"

CATEGORIES = ["freshapple", "freshbanana", "freshorange", 
              "rottenapple", "rottenbanana", "rottenorange"]

#https://wandb.ai/authorize
os.getenv("WANDB_API_KEY")
wandb.login()

#https://wandb.ai/antonios-org/fruit-classifier/artifacts/model/resnet18/v2
wandb_org = os.getenv('WANDB_ORG')
wandb_project = os.getenv('WANDB_PROJECT')


from torch import nn
from torchvision import transforms
from torchvision.models import resnet18, ResNet


def get_raw_model() -> ResNet:
    # overwrite final classifier layer with our own output layers
    N_CLASSES = 6

    model = resnet18(weights=None)
    model.fc = nn.Sequential(
        nn.Linear(512, 512),
        nn.ReLU(),
        nn.Linear(512, N_CLASSES)
    )

    return model


def load_model() -> ResNet:
    model = get_raw_model()
    model_state_dict_path = os.path.join(MODELS_DIR, MODEL_FILE_NAME)
    model_state_dict = torch.load(model_state_dict_path, map_location="cpu")
    model.load_state_dict(model_state_dict, strict=False)
    model.eval()

    return model


def load_transforms() -> transforms.Compose:
    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])


# fastapi run app/main_local.py --port 8080 
class Result(BaseModel):
    label: str
    prob: float


app = FastAPI()


@app.post("/predict", response_model=Result)
async def predict(
        input_image: UploadFile = File(...),
        model: ResNet = Depends(load_model),
        transforms: transforms.Compose = Depends(load_transforms)
) -> Result:
    # Read the uploaded image
    image = Image.open(io.BytesIO(await input_image.read()))

    # Convert RGBA image to RGB image
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Apply the transformations
    image = transforms(image).unsqueeze(0)  # Add batch dimension

    # Make the prediction
    with torch.no_grad():
        outputs = model(image)
        probabilities = F.softmax(outputs[0], dim=0)
        prob, predicted_class = torch.max(probabilities, 0)

    # Map the predicted class index to the category
    label = CATEGORIES[predicted_class.item()]

    return Result(label=label, prob=prob.item())