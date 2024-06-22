from dotenv import load_dotenv
import os
import wandb 


load_dotenv()

#https://wandb.ai/authorize
os.getenv("WANDB_API_KEY")
wandb.login()

#https://wandb.ai/antonios-org/fruit-classifier/artifacts/model/resnet18/v2
wandb_org = os.getenv('WANDB_ORG')
wandb_project = os.getenv('WANDB_PROJECT')

print(wandb_org)


wandb_org = os.getenv("WANDB_ORG")
wandb_project = os.getenv("WANDB_PROJECT")
wandb_model_name = os.getenv("WANDB_MODEL_NAME")
wandb_model_version = os.getenv("WANDB_MODEL_VERSION")

artifact_path = f"{wandb_org}/{wandb_project}/{wandb_model_name}:{wandb_model_version}"
artifact = wandb.Api().artifact(artifact_path, type="model")

MODELS_DIR='models'
artifact.download(root=MODELS_DIR)