# ProDev Nexus E-Commerce Backend

## Overview

The ProDev Nexus E-Commerce Backend is a production-grade, scalable API built for modern e-commerce platforms. It leverages Django 5 and Django REST Framework to provide a robust suite of features including secure authentication, product management, real-time notifications, and atomic order processing.

The system is designed with data integrity and concurrency in mind, utilizing atomic transactions, row-level locking, and asynchronous background processing. It is fully containerized and ready for orchestration via Kubernetes.

## Key Features

- **Authentication**: Secure JWT-based auth with custom user models and role-based access control (Admin vs. Customer).
- **Product Catalog**: Advanced CRUD with image uploads (Cloudinary), soft-delete functionality, and filtering (price, category, stock).
- **Shopping Cart**: Persistent server-side cart with atomic stock validation to prevent race conditions.
- **Order Processing**: Atomic order creation with price snapshotting and automatic stock adjustment.
- **Notifications**: Dual-channel system (In-App + Email) powered by Celery & RabbitMQ.
- **Infrastructure**: Fully dockerized environment with Nginx/Gunicorn, PostgreSQL, Redis, and RabbitMQ.
- **CI/CD**: Automated testing and deployment pipelines using GitHub Actions and Jenkins.

## Technology Stack

- **Language**: Python 3.11
- **Framework**: Django 5.x, Django REST Framework
- **Database**: PostgreSQL 15
- **Caching & Broker**: Redis
- **Message Queue**: RabbitMQ
- **Asynchronous Tasks**: Celery
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes (K8s)
- **CI/CD**: Jenkins, GitHub Actions

## Project Structure

```
prodev-ecommerce-backend/
├── src/               # Application Source Code
│   ├── core/          # Project settings & config
│   ├── accounts/      # User management & Auth
│   ├── products/      # Product catalog & Images
│   ├── carts/         # Shopping cart logic
│   ├── orders/        # Order processing
│   └── notifications/ # In-app alerts
├── infra/             # Infrastructure Configuration
│   ├── docker/        # Dockerfiles & Compose
│   ├── k8s/           # Kubernetes Manifests
│   └── jenkins/       # Local Jenkins Server
├── docs/              # Detailed Documentation
│   ├── diagrams/      # Architecture & ERD
│   └── api/           # Postman Collections
└── scripts/           # Automation Scripts
```

## Setup & Installation

### Option 1: Docker (Recommended)

This sets up the entire stack (Web, DB, Redis, RabbitMQ) automatically.

**Clone the Repo:**

```bash
git clone <repo-url>
cd prodev-ecommerce-backend
```

**Configure Environment:**

```bash
cd infra/docker
cp .env.example .env
# Ensure POSTGRES_HOST=db in .env
```

**Start Services:**

```bash
docker compose up --build -d
```

**Initialize App:**

```bash
docker compose exec web python src/manage.py migrate
docker compose exec web python src/manage.py createsuperuser
```

### Option 2: Local Python Environment

See `docs/README.md` for manual installation steps.

## Documentation

### API Specification

- **Swagger UI**: http://localhost:8000/docs/
- **ReDoc**: http://localhost:8000/redoc/
- **Postman Collection**: Available in `docs/api/postman_collection.json`

### Architecture

Database Schema (ERD) and System Design notes are located in the `docs/` directory.

## Testing & CI/CD

The project enforces code quality via automated pipelines.

### Running Tests Locally

```bash
# Run all unit tests
docker compose exec web python src/manage.py test src

# Run integration tests (requires Docker)
bash scripts/test_api.sh
```

### Pipelines

- **GitHub Actions**: Runs linting (flake8) and unit tests on every Pull Request.
- **Jenkins**: Handles building Docker images and deploying to Kubernetes on merge to main.

## Future Roadmap

While the core e-commerce functionality is complete, the following features are planned for the next major release:

### 1. Payment Integration

- **Stripe/PayPal API**: Secure payment processing.
- **Webhooks**: Handling payment success/failure events asynchronously.
- **Refunds**: Admin dashboard for processing refunds.

### 2. Product Reviews & Ratings

- **User Feedback**: Allow verified purchasers to leave text reviews and star ratings.
- **Aggregations**: Calculate average product ratings dynamically.
- **Moderation**: Admin tools to approve/flag reviews.

### 3. Wishlist Functionality

- **Saved Items**: Allow users to save products for later without adding them to the cart.
- **Stock Alerts**: Notify users when wishlist items come back in stock.

### 4. Advanced Search

- **Elasticsearch**: Integration for full-text search, fuzzy matching, and faster filtering for large catalogs.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'feat: add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.
