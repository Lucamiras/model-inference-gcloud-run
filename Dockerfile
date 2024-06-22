# https://fastapi.tiangolo.com/deployment/docker/
# Use the official Python slim image
FROM python:3.11-slim

# Set the working directory
WORKDIR /code

# Copy the requirements file
COPY ./requirements.txt /code/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code
COPY ./app /code/app

# Set environment variables

ENV WANDB_API_KEY="" 
ENV WANDB_ORG="antonios-org"
ENV WANDB_PROJECT="fruit-classifier"
ENV WANDB_MODEL_NAME="resnet18"
ENV WANDB_MODEL_VERSION="v2"

# Command to run the application
CMD ["fastapi", "run", "app/main.py", "--port", "8080"]

#Breakdown 
#Here's an explanation of the Dockerfile line by line, followed by instructions on how to run it.
#
#```dockerfile
## https://fastapi.tiangolo.com/deployment/docker/
## Use the official Python slim image
#FROM python:3.11-slim
#```
#- **FROM python:3.11-slim**: This line specifies the base image to use for the Docker container, which is a lightweight version of Python 3.11.
#
#```dockerfile
## Set the working directory
#WORKDIR /code
#```
#- **WORKDIR /code**: This line sets the working directory inside the container to `/code`. All subsequent commands will be run from this directory.
#
#```dockerfile
## Copy the requirements file
#COPY ./requirements.txt /code/requirements.txt
#```
#- **COPY ./requirements.txt /code/requirements.txt**: This line copies the `requirements.txt` file from your local machine to the `/code` directory inside the container.
#
#```dockerfile
## Install the dependencies
#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#```
#- **RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt**: This line installs the Python dependencies listed in the `requirements.txt` file. The `--no-cache-dir` option prevents the creation of a cache directory for pip.
#
#```dockerfile
## Copy the application code
#COPY ./app /code/app
#```
#- **COPY ./app /code/app**: This line copies the `app` directory from your local machine to the `/code/app` directory inside the container.
#
#```dockerfile
## Set environment variables
#ENV WANDB_API_KEY=""
#ENV WANDB_ORG=""
#ENV WANDB_PROJECT=""
#ENV WANDB_MODEL_NAME=""
#ENV WANDB_MODEL_VERSION=""
#```
#- **ENV WANDB_API_KEY=""** and similar lines: These lines set environment variables within the container. These are placeholders for API keys and other configurations for Weights & Biases (wandb).
#
#```dockerfile
## Command to run the application
#CMD ["fastapi", "run", "app/main.py", "--port", "8080"]
#```
#- **CMD ["fastapi", "run", "app/main.py", "--port", "8080"]**: This line specifies the command to run the FastAPI application when the container starts. It runs the `main.py` script in the `app` directory on port 8080.
#
#### How to run it
#
#1. **Build the Docker image:**
#   Open your terminal and navigate to the directory containing the Dockerfile. Run the following command to build the Docker image:
#
#   ```sh
#   docker build -t my-fastapi-app .
#   ```
#
#2. **Run the Docker container:**
#   After building the image, you can run the container with the following command:
#
#   ```sh
#   docker run -d -p 8080:8080 my-fastapi-app
#   ```
#
#   - `-d`: Run the container in detached mode.
#   - `-p 8080:8080`: Map port 8080 of the container to port 8080 on your local machine.
#
#After running the container, your FastAPI application should be accessible at `http://localhost:8080`.