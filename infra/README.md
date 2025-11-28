
# Infrastructure Configuration

This directory contains the configuration files for containerization, orchestration, and deployment of the **ProDev E-Commerce Backend**.

## Directory Structure

```

infra/
├── docker/
│   ├── .env                # Environment variables for Docker services
│   ├── docker-compose.yml  # Service orchestration (Local Dev)
│   └── Dockerfile          # Python application image definition
└── k8s/                    # Kubernetes manifests (Production/Staging)
├── configmap.yaml      # Non-sensitive env vars
├── secret.yaml         # Sensitive secrets (encoded)
├── postgres.yaml       # StatefulSet for Database
├── redis.yaml          # Deployment for Cache
├── rabbitmq.yaml       # Deployment for Broker
├── web.yaml            # Deployment for Django App
└── celery.yaml         # Deployment for Workers

```

---

## Live Environment

### Evaluators & Testers:
If you simply wish to test the functionality of the application, please use the *live deployed version* instead of deploying your own cluster.

- **API Documentation:**  
  `http://[YOUR_LIVE_IP_OR_DOMAIN]/docs/`

- **Admin Panel:**  
  `http://[YOUR_LIVE_IP_OR_DOMAIN]/admin/`

---

## Docker Compose (Local Development)

The Docker setup orchestrates the following services locally:

| Service        | Description                      | Internal Port | External Port |
|----------------|----------------------------------|---------------|----------------|
| web            | Django App (Gunicorn)            | 8000          | 8000           |
| db             | PostgreSQL 15 Database           | 5432          | -              |
| redis          | Cache & Message Broker           | 6379          | -              |
| rabbitmq       | Celery Broker                    | 5672, 15672   | 5672, 15672    |
| celery_worker  | Background task worker           | --            | --             |
| celery_beat    | Periodic task scheduler          | --            | --             |

---

### 1. Environment Variables

The `infra/docker/.env` file is critical.  
Ensure **POSTGRES_HOST** matches the service name in `docker-compose.yml`.

**Required Settings:**

```

POSTGRES_HOST=db
POSTGRES_PORT=5432
CELERY_BROKER_URL=amqp://admin:admin@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0
REDIS_URL=redis://redis:6379/1
DJANGO_SETTINGS_MODULE=src.core.settings

```

---

### 2. Management Commands

Run these from **infra/docker**.

#### Start the stack
```

docker compose up -d

```

#### Rebuild images (after code changes)
```

docker compose up --build -d

```

#### Execute commands inside the container  
(For migrations, superuser creation, tests)

```

docker compose exec web python src/manage.py migrate

```

#### Stop the stack and reset data
```

docker compose down -v

```

---

## Kubernetes Configuration

This section explains how to deploy the application on a Kubernetes cluster (Minikube, EKS, etc.).

### Important Note for Testers
Do **NOT** push images to the project’s official Docker Hub repository.

If you want to test deployment, use **your own Docker Hub username**.

---

### 1. Build and Push Image

Login to Docker Hub:

```

docker login

```

Build and tag the image (replace *your-username*):

```

# Run from project root

docker build -t your-username/prodev-backend:latest -f infra/docker/Dockerfile .

```

Push to registry:

```

docker push your-username/prodev-backend:latest

```

---

### 2. Update Kubernetes Manifests

Before applying, update the image name in:

- `infra/k8s/web.yaml`
- `infra/k8s/celery.yaml`

Change:

```

image: original-repo/prodev-backend:latest

```

to:

```

image: your-username/prodev-backend:latest

```

---

### 3. Deploy to Cluster

Apply in this order:

```

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

---

### 4. Initialize Database

Run migrations inside a temporary pod:

```

kubectl run migration-job --rm -it 
--image=your-username/prodev-backend:latest 
--env-from=configmap/backend-config 
--env-from=secret/backend-secrets 
--restart=Never 
-- python src/manage.py migrate

```

---

### 5. Access the Application

**On Minikube:**

```

minikube service web

```

**On Cloud Providers:**

Get external IP:

```

kubectl get svc web

```

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'accounts'`

Ensure the `PYTHONPATH` is set correctly in `docker-compose.yml` or `k8s/web.yaml`:

```

env:

* name: PYTHONPATH
  value: "/app:/app/src"

