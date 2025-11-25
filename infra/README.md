# Infrastructure Configuration

This directory contains the configuration files for containerization, orchestration, and deployment of the ProDev E-Commerce Backend.

## Directory Structure

```
infra/
├── docker/
│   ├── .env                # Environment variables for Docker services
│   ├── docker-compose.yml  # Service orchestration
│   └── Dockerfile          # Python application image definition
└── k8s/                    # Kubernetes manifests (Planned)
```

## Docker Configuration

The Docker setup orchestrates the following services:

| Service        | Description                      | Internal Port | External Port |
|----------------|----------------------------------|---------------|---------------|
| web            | Django Application (Gunicorn)    | 8000          | 8000          |
| db             | PostgreSQL 15 Database           | 5432          | -             |
| redis          | Redis (Cache & Message Broker)   | 6379          | -             |
| rabbitmq       | RabbitMQ (Celery Broker)         | 5672, 15672   | 5672, 15672   |
| celery_worker  | Background task worker           | -             | -             |
| celery_beat    | Periodic task scheduler          | -             | -             |

## Environment Variables (.env)

The `infra/docker/.env` file is critical for connecting services. Ensure the `POSTGRES_HOST` matches the service name defined in `docker-compose.yml`.

**Critical Settings:**

```
POSTGRES_HOST=db
POSTGRES_PORT=5432
CELERY_BROKER_URL=amqp://admin:admin@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0
REDIS_URL=redis://redis:6379/1
DJANGO_SETTINGS_MODULE=src.core.settings
```

## Management Commands

Run these commands from the `infra/docker` directory.

**Start the stack**
```bash
docker compose up -d
```

**Rebuild images (after code changes)**
```bash
docker compose up --build -d
```

**View Application Logs**
```bash
docker compose logs -f web
```

**Execute Commands in Container**

To run Django management commands (migrations, superuser creation, tests):
```bash
docker compose exec web python src/manage.py <command>
```

Example: 
```bash
docker compose exec web python src/manage.py migrate
```

**Stop the stack**
```bash
docker compose down
```

**Stop and remove volumes (Resets Database)**
```bash
docker compose down -v
```

## Troubleshooting

### ModuleNotFoundError: No module named 'accounts'

Ensure the `PYTHONPATH` is correctly set in the `docker-compose.yml` environment section:

```yaml
environment:
  PYTHONPATH: /app:/app/src
```

### Database Connection Errors

If the application cannot connect to the database, verify that `POSTGRES_HOST` in `.env` is set to `db` (the Docker service name), not `localhost`.
