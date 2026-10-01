# AI Solutions Portfolio

This repository contains a simple Flask-based web application that fetches and displays NASA's Astronomy Picture of the Day (APOD). The project is designed to demonstrate a full Python app lifecycle including local development, containerization with Docker, CI/CD with Jenkins, and deployment on Kubernetes.

## Project Overview

The app calls the NASA APOD API and renders the returned image or media content in a browser. It uses:

- Python
- Flask
- Requests
- python-dotenv
- Docker
- Kubernetes
- Jenkins

## Project Structure

```text
ai-solutions-portfolio/
├── .env
├── .gitignore
├── Dockerfile
├── Jenkinsfile
├── README.md
├── requirements.txt
├── nasa-app.py
├── index.html
├── templates/
│   └── index.html
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
└── .venv/
```

## Key Files

### `nasa-app.py`
Main Flask application entry point.

- Creates the Flask app
- Loads environment variables from `.env`
- Calls the NASA API
- Passes APOD content into the template
- Runs the app on port `5000`

### `requirements.txt`
Lists the project's Python dependencies:

```txt
Flask==3.1.3
python-dotenv==1.2.4
requests==2.32.5
```

### `templates/index.html`
HTML template used to render the APOD details, including:

- title
- date
- image or media link
- explanation
- credit information

### `Dockerfile`
Docker build definition for the Python app.

### `Jenkinsfile`
Simplified CI pipeline that checks out the repo and builds the Docker image.

### `k8s/deployment.yaml`
Kubernetes deployment for the app with 2 replicas.

### `k8s/service.yaml`
Kubernetes Service exposing the app via a NodePort.

## Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.10+
- pip
- Docker
- Kubernetes cluster or Minikube
- Git

## Local Development Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd ai-solutions-portfolio
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your NASA API key:

```env
NASA_API_KEY=your_nasa_api_key_here
```

5. Run the app locally:

```bash
python nasa-app.py
```

The app will run on:

```text
http://localhost:5000
```

## Docker Setup

Build the Docker image:

```bash
docker build -t nasa-app:1.0 .
```

Run the container locally:

```bash
docker run -p 5000:5000 --env-file .env nasa-app:1.0
```

Then open:

```text
http://localhost:5000
```

## Jenkins CI Pipeline

The `Jenkinsfile` performs the following stages:

- Checkout source code
- Build stage
- Docker image build stage

Run the pipeline from a Jenkins environment using the repo as the source.

## Kubernetes Deployment

The Kubernetes manifests are located in the `k8s/` directory.

### Deploy the application

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Verify the deployment

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

The service exposes the app through a NodePort on port `30080`:

```text
http://<node-ip>:30080
```

## Application Behavior

The app loads the latest APOD entry from NASA and renders it in the browser. If the media is an image, it is displayed directly; otherwise, a link is shown to view the NASA content.

## Environment Variables

| Variable | Required | Description |
| --- | --- | --- |
| `NASA_API_KEY` | Yes | API key used to access the NASA APOD API |

## Notes

- Keep `.env` out of source control if it contains sensitive credentials.
- The repo already includes `.env` in `.gitignore`.
- This project is a simple demonstration app and is not intended for production-grade deployment without additional hardening.

## Troubleshooting

### App fails to start

- Make sure `.env` exists and contains `NASA_API_KEY`
- Confirm dependencies are installed
- Verify Flask is running in the correct Python environment

### Docker build fails

- Ensure Docker is running
- Check that the `requirements.txt` file is present
- Verify the `Dockerfile` has the correct working directory and file paths

### Kubernetes service is not reachable

- Confirm pods are running
- Check `kubectl get endpoints`
- Make sure the service selector matches the deployment labels

## License

This project is for educational and portfolio/demo purposes.
