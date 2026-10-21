
# Student Information Portal - CI/CD Project

## Project Overview
This project demonstrates an automated CI/CD pipeline
for an existing Flask student application.

The application was originally developed as part of
the Cloud Computing and DevOps Laboratory.

## Technologies
- Python and Flask
- GitHub
- Jenkins
- Docker
- Docker Hub
- AWS EC2
- Kubernetes and Minikube

## Application Endpoints
- `/` - Home page
- `/student` - Student information

## Local Execution
Install dependencies:

    python -m pip install -r requirements.txt

Run the application:

    python app.py

Open http://localhost:5000

## Automated Testing
Run:

    python -m pytest -v

## Docker
Build:

    docker build -t student-cicd:v1 .

Run:

    docker run -p 5000:5000 student-cicd:v1

## CI/CD Pipeline
The planned Jenkins pipeline will:
1. Pull source code from GitHub.
2. Build and test the application.
3. Build a Docker image.
4. Push the image to Docker Hub.
5. Deploy the image to Minikube.
6. Verify the application.

## Deployment Status
Local Flask and Docker testing completed.
Jenkins and Kubernetes integration pending.

## Version
Version 1.0
