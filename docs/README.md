# Documentation Overview

This directory contains all architectural, design, and development documentation for the **ProDev E-Commerce Backend** project. It serves as the central reference point for contributors, frontend developers, DevOps engineers, and reviewers.

## Folder Structure

```

docs/
│
├── diagrams/
│    ├── erd.png
│    └── architecture.png (Planned)
│
├── api/
│    └── postman_collection.json
│
└── README.md

```

---

## 1. Entity Relationship Diagram (ERD)

The ERD provides a complete overview of all database entities and their relationships, including:

- Users (Custom Model)  
- Categories & Products  
- Cart & Cart Items  
- Orders & Order Items  
- Addresses & Notifications  

**Location:** `docs/diagrams/erd.png`

---

## 2. Architecture Notes

This section outlines the core technical decisions and architectural patterns used in the system.

### Backend Architecture (Django + DRF)

The system is built on **Django 5** and **Django REST Framework (DRF)**, using a modular, domain-driven design approach.

Key architectural decisions:

- **App-Based Structure:** Functionality is separated into independent apps (accounts, products, orders, notifications) to maintain separation of concerns.  
- **ViewSets:** Use of `ModelViewSet` to standardize CRUD operations and reduce boilerplate.  
- **Serializers:** Nested serializers provide rich API responses (e.g., orders include items and product details).  
- **Service Layer Pattern:** Complex business logic (e.g., atomic order creation, stock adjustments) is placed in model methods or service functions to keep views simple.

**Location:** `docs/diagrams/architectural-diagram.png`
---

### Authentication & Authorization (JWT)

Security is implemented using **JSON Web Tokens (JWT)** via the `simplejwt` library.

- **Stateless Authentication:** The server holds no session state, improving scalability.  
- **Token Lifecycle:**  
  - Access Token: Short-lived (15 minutes) for API authorization  
  - Refresh Token: Long-lived (7 days) for obtaining new access tokens  
- **RBAC (Role-Based Access Control):** Custom permissions (e.g., `IsAdminOrReadOnly`) enforce strict access rules between Customers and Administrators.

---

### Asynchronous Processing (Celery + RabbitMQ)

To maintain fast API responses, heavy tasks are offloaded to background workers.

- **Broker:** RabbitMQ queues tasks from Django.  
- **Worker:** Celery workers process queued tasks asynchronously.  
- **Use Cases:**  
  - Sending welcome emails  
  - Sending "New Product" alerts  
  - Periodic database cleanup (Celery Beat)

---

### File Storage Strategy

Media files (e.g., product images) are handled differently in development and production.

- **Local (Development):** Stored in a `media/` volume.  
- **Cloud (Production):** Stored using Cloudinary for persistence and CDN delivery.

Reason: Kubernetes pods are ephemeral; local files are wiped on restart, so cloud storage ensures persistence.

---

### Notification Workflow

The system uses a hybrid notification strategy:

- **In-App Notifications:**  
  - Stored in PostgreSQL  
  - Users can poll via API  
  - Mark as read (single or bulk)

- **Email Notifications:**  
  - Sent asynchronously via Celery  
  - Reserved for critical alerts

---

### CI/CD Pipeline (GitHub Actions + Jenkins)

The system uses a split continuous integration and deployment pipeline.

#### GitHub Actions (CI)

Triggered on every Pull Request:

- Runs linting (`flake8`)  
- Executes unit tests (`python manage.py test`)  
- Blocks merge if tests fail  

#### Jenkins (CD)

Triggered on merge to `main`:

- Builds Docker image  
- Pushes image to Docker Hub  
- Performs a rolling update on the Kubernetes cluster  

---

### Deployment Model (Docker + Kubernetes)

The application is cloud-agnostic and scalable.

#### Containerization

- Multi-stage Dockerfile  
- Produces a lightweight production-ready image running Gunicorn  

#### Kubernetes

- **Stateless Apps:** Django Web and Celery Workers run as Deployments (ReplicaSets)  
- **Stateful Services:** PostgreSQL, Redis, RabbitMQ run as StatefulSets with PVCs  
- **Configuration Management:** ConfigMaps and Secrets store environment variables, keeping sensitive values out of the image  

---

## 3. API Documentation

Complete API documentation is auto-generated and interactive.

- **Swagger UI:** `/docs/`  
- **ReDoc:** `/redoc/`  
- **Postman Collection:** `docs/api/postman_collection.json`  

---

## 4. System Workflows

### User Registration Flow

1. User submits credentials to `/api/auth/register/`.  
2. Server validates data and creates the User record.  
3. Celery task sends a welcome email.  
4. In-app welcome notification is created.  
5. API returns **HTTP 201 Created**.

---

### Order Creation Flow

1. User submits checkout request.  
2. Atomic transaction begins; stock rows are locked.  
3. Server validates stock availability.  
4. Order and OrderItem records are created.  
5. Product prices are duplicated into OrderItem to freeze cost.  
6. Cart is cleared.  
7. In-app notification "Order Placed" is generated.  
8. Transaction commits.  

