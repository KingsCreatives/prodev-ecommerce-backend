# ProDev Nexus E-Commerce Backend

**Live Demo URL:** [https://prodev-backend.onrender.com/](https://prodev-backend.onrender.com/)

---

## 🚀 Overview

ProDev Nexus is a production-grade, scalable API built for modern e-commerce platforms. It leverages Django 5 and Django REST Framework to provide a robust suite of features including secure authentication, product management, real-time notifications, and atomic order processing.

The system is designed with data integrity and concurrency in mind, utilizing atomic transactions, row-level locking, and asynchronous background processing via Celery & Redis. It is fully containerized and ready for cloud deployment.

---

## 🎥 Video Demo

Watch the system in action: **Async Order Processing & Architecture Walkthrough**

**Video Demo URL:** [prodev-backend-video-demo](https://drive.google.com/file/d/1eghL44hZWWijs1ka9fRg-dkeAUtEI19d/view?usp=drive_link)

---

## ⚡ Key Features

- **Authentication:** Secure JWT-based auth (Access/Refresh tokens) with custom user models and role-based access control (Admin vs. Customer).
- **Product Catalog:** Advanced CRUD with image uploads (Cloudinary), soft-delete functionality, and filtering (price, category, stock).
- **Asynchronous Processing:** Heavy tasks (like email notifications) are offloaded to background workers using Celery & Redis, ensuring the API responds in <200ms.
- **Order Processing:** Atomic order creation with nested item support, price snapshotting, and automatic stock adjustment.
- **Notifications:** Dual-channel system (In-App + Email) powered by Celery.
- **Infrastructure:** Fully dockerized environment with Nginx/Gunicorn, PostgreSQL, Redis, Celery Workers and RabbitMQ.
- **CI/CD**: Automated testing and deployment pipelines using GitHub Actions and Jenkins.
- **Developer Hub:** Includes a dedicated landing page and interactive Swagger documentation.

---

## 🛠️ Technology Stack

| Component      | Technology      | Role                           |
| -------------- | --------------- | ------------------------------ |
| Language       | Python 3.11     | Core logic                     |
| Framework      | Django 5 + DRF  | API framework                  |
| Database       | PostgreSQL 15   | Relational data store          |
| Async Queue    | Celery 5        | Task queue manager             |
| Message Broker | Redis 7         | In-memory broker for Celery    |
| Deployment     | Docker & Render | Container orchestration & PaaS |
| Media          | Cloudinary      | Cloud image storage            |

---

## 🌍 Deployment Notes (Render Free Tier)

This application is deployed on the **Render Free Tier**. Please be aware of the following limitations when testing:

- **Cold Start Latency:** The server "sleeps" after 15 minutes of inactivity. The first request may take up to 50 seconds to wake up the instance. Please be patient; subsequent requests will be instant.
- **Resource Limits:** The free instance has 512MB RAM. Heavy image uploads may occasionally time out.

### Live Endpoints:

- **Landing Page:** [https://prodev-backend.onrender.com/](https://prodev-backend.onrender.com/)
- **Swagger Docs:** [https://prodev-backend.onrender.com/api/docs/](https://prodev-backend.onrender.com/api/docs/)
- **Admin Panel:** [https://prodev-backend.onrender.com/api/admin/](https://prodev-backend.onrender.com/api/admin/)

---

## 🔧 Local Setup Guide

Follow these steps to run the project on your machine.

### Prerequisites

- Docker & Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/KingsCreatives/prodev-ecommerce-backend.git
cd prodev-ecommerce-backend
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory (or `infra/docker/` depending on your setup):

```bash
# Core
DJANGO_SECRET_KEY=unsafe-secret-key-for-dev
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=ecommerce
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis & Celery
REDIS_URL=redis://redis:6379/1
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Cloudinary (Optional for local dev, required for images)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 3. Start with Docker

Run the entire stack (Django, Postgres, Redis, Celery) with one command:

```bash
docker-compose up --build
```

### 4. Initialize Database

Once the containers are running, apply migrations and create a superuser:

```bash
# Run migrations
docker-compose exec web python src/manage.py migrate

# Create Admin User
docker-compose exec web python src/manage.py createsuperuser
```

The API will be available at **http://localhost:8000/**.

---

## 🧪 Testing the API

You can test the API using the included Postman Collection or via the Swagger UI.

### Main Workflows

1. **Register:** `POST /api/auth/register/`
2. **Login:** `POST /api/auth/login/` (Copy the access token)
3. **Create Product (Admin):** `POST /api/products/`
4. **Place Order:** `POST /api/orders/`

**Note:** Check your terminal logs to see the async email task execute!

---

## 📂 Project Structure

```
prodev-ecommerce-backend/
├── src/               # Application Source Code
│   ├── core/          # Project settings & config
│   ├── accounts/      # User management & Auth
│   ├── products/      # Product catalog & Images
│   ├── carts/         # Shopping cart logic
│   ├── orders/        # Order processing
│   ├── notifications/ # Celery Tasks (Email)
│   └── templates/     # HTML Landing Page
├── infra/             # Infrastructure Configuration
│   ├── docker/        # Dockerfiles & Compose
├── docs/              # Detailed Documentation
│   ├── api/           # Postman Collections
└── scripts/           # Automation Scripts
```

---

## Future Roadmap

While the core e-commerce functionality is complete, the following features are planned for the next major release:

- **Payment Integration:** Stripe/PayPal API integration with webhooks.
- **Product Reviews:** User feedback and star ratings.
- **Advanced Search:** Elasticsearch integration for full-text search.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'feat: add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.
