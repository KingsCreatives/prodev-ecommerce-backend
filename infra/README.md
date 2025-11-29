# Infrastructure Configuration

This directory contains the configuration files for containerization, orchestration, and deployment of the ProDev E-Commerce Backend.

## Directory Structure

```
infra/
├── docker/
│   ├── .env                # Environment variables for Docker services
│   ├── docker-compose.yml  # Service orchestration (Local Dev)
│   └── Dockerfile          # Python application image definition
├── jenkins/
│   ├── docker-compose.yml  # Jenkins server orchestration
│   └── Dockerfile          # Custom Jenkins image with Docker CLI & Kubectl
└── k8s/                    # Kubernetes manifests (Production/Staging)
    ├── configmap.yaml      # Non-sensitive env vars
    ├── secret.yaml         # Sensitive secrets (encoded)
    ├── postgres.yaml       # StatefulSet for Database
    ├── redis.yaml          # Deployment for Cache
    ├── rabbitmq.yaml       # Deployment for Broker
    ├── web.yaml            # Deployment for Django App
    └── celery.yaml         # Deployment for Workers

.github/
└── workflows/
    └── ci.yml              # GitHub Actions CI Pipeline
```

## Live Environment

**Evaluators & Testers:**

If you simply wish to test the functionality of the application, please use the live deployed version instead of deploying your own cluster.

- **API Documentation:** http://[YOUR_LIVE_IP_OR_DOMAIN]/docs/
- **Admin Panel:** http://[YOUR_LIVE_IP_OR_DOMAIN]/admin/

## Docker Compose (Local Development)

The Docker setup orchestrates the following services locally:

| Service | Description | Internal Port | External Port |
|---------|-------------|---------------|---------------|
| web | Django App (Gunicorn) | 8000 | 8000 |
| db | PostgreSQL 15 Database | 5432 | - |
| redis | Cache & Message Broker | 6379 | - |
| rabbitmq | Celery Broker | 5672, 15672 | 5672, 15672 |
| celery_worker | Background task worker | - | - |
| celery_beat | Periodic task scheduler | - | - |

### 1. Environment Variables

The `infra/docker/.env` file is critical. Ensure `POSTGRES_HOST` matches the service name in `docker-compose.yml`.

**Required Settings:**

```
POSTGRES_HOST=db
POSTGRES_PORT=5432
CELERY_BROKER_URL=amqp://admin:admin@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0
REDIS_URL=redis://redis:6379/1
DJANGO_SETTINGS_MODULE=src.core.settings
```

### 2. Management Commands

Run these from `infra/docker`.

**Start the stack**

```bash
docker compose up -d
```

**Rebuild images (after code changes)**

```bash
docker compose up --build -d
```

**Execute commands inside the container**

(For migrations, superuser creation, tests)

```bash
docker compose exec web python src/manage.py migrate
```

**Stop the stack and reset data**

```bash
docker compose down -v
```

## GitHub Actions CI Pipeline

The project uses GitHub Actions for automated testing and linting on every push and pull request to `main` and `develop` branches.

### Pipeline Features

- **Automated Testing:** Runs Django tests with PostgreSQL and Redis services
- **Code Linting:** Uses Flake8 to check for syntax errors and code quality
- **Service Orchestration:** Automatically spins up PostgreSQL and Redis containers
- **Python 3.11:** Tests run on the latest Python version

### Workflow Triggers

The CI pipeline runs automatically on:
- Push to `main` or `develop` branches
- Pull requests targeting `main` or `develop` branches

### Manual Test Execution

To run tests locally with the same environment:

```bash
# Set environment variables
export SECRET_KEY="test-secret-key"
export DEBUG="True"
export POSTGRES_DB=ecommerce_test
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=password
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export CELERY_BROKER_URL="redis://localhost:6379/0"
export CELERY_RESULT_BACKEND="redis://localhost:6379/0"
export DJANGO_SETTINGS_MODULE="src.core.settings"

# Run tests
python src/manage.py test src
```

### Linting

To run Flake8 linting locally:

```bash
# Install flake8
pip install flake8

# Check for critical errors
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Check all issues (warnings)
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

## Jenkins CI/CD Setup

To run a local Jenkins server that can build Docker images and deploy to Kubernetes:

### 1. Start Jenkins

Run from `infra/jenkins`:

```bash
docker compose up -d --build
```

### 2. Initial Setup

Retrieve the initial admin password:

```bash
# For Git Bash users (Windows)
MSYS_NO_PATHCONV=1 docker exec prodev-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Access Jenkins at http://localhost:8080.

### 3. Configuration

- Install recommended plugins.
- Add Docker Hub credentials with ID: `docker-hub-credentials`.
- Create a Pipeline job pointing to your Git repository's Jenkinsfile.

## Kubernetes Configuration

This section explains how to deploy the application on a Kubernetes cluster (Minikube, EKS, etc.).

### Important Note for Testers

**Do NOT push images to the project's official Docker Hub repository.**

If you want to test deployment, use your own Docker Hub username.

### 1. Build and Push Image

**Login to Docker Hub:**

```bash
docker login
```

**Build and tag the image (replace your-username):**

```bash
# Run from project root
docker build -t your-username/prodev-backend:latest -f infra/docker/Dockerfile .
```

**Push to registry:**

```bash
docker push your-username/prodev-backend:latest
```

### 2. Update Kubernetes Manifests

Before applying, update the image name in:

- `infra/k8s/web.yaml`
- `infra/k8s/celery.yaml`

Change:

```yaml
image: original-repo/prodev-backend:latest
```

to:

```yaml
image: your-username/prodev-backend:latest
```

### 3. Deploy to Cluster

Apply in this order:

```bash
# 1. Configs & Secrets
kubectl apply -f infra/k8s/configmap.yaml
kubectl apply -f infra/k8s/secret.yaml

# 2. Backing Services
kubectl apply -f infra/k8s/postgres.yaml
kubectl apply -f infra/k8s/redis.yaml
kubectl apply -f infra/k8s/rabbitmq.yaml

# 3. Application Services
kubectl apply -f infra/k8s/web.yaml
kubectl apply -f infra/k8s/celery.yaml
```

### 4. Initialize Database

Run migrations inside a temporary pod:

```bash
kubectl run migration-job --rm -it \
  --image=your-username/prodev-backend:latest \
  --env-from=configmap/backend-config \
  --env-from=secret/backend-secrets \
  --restart=Never \
  -- python src/manage.py migrate
```

### 5. Access the Application

**On Minikube:**

```bash
minikube service web
```

**On Cloud Providers:**

Get external IP:

```bash
kubectl get svc web
```

## Troubleshooting

**ModuleNotFoundError: No module named 'accounts'**

Ensure the `PYTHONPATH` is set correctly in `docker-compose.yml` or `k8s/web.yaml`:

```yaml
env:
  - name: PYTHONPATH
    value: "/app:/app/src"
```