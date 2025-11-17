# ProDev E-Commerce Backend

## Overview
The **ProDev Nexus E-Commerce Backend** is a fully functional backend system for an e-commerce platform. It demonstrates advanced backend development skills using **Django**, **PostgreSQL**, and **Django REST Framework**.  

This project simulates a real-world environment and includes:

- CRUD APIs for products, categories, and users
- JWT-based authentication and authorization
- Filtering, sorting, and pagination for product discovery
- API documentation using **Swagger/OpenAPI**
- Plans for background tasks, container orchestration, and CI/CD

---

## Project Goals

- Build scalable and maintainable backend architecture
- Implement secure user authentication
- Optimize database design and queries
- Document APIs for frontend consumption
- Prepare for real-world deployment (Docker, Kubernetes, Jenkins)

---

## Technologies Used

- **Backend:** Django, Django REST Framework  
- **Database:** PostgreSQL  
- **Authentication:** JWT (JSON Web Tokens)  
- **API Documentation:** Swagger / DRF-YASG  
- **Task Queue (future):** Celery + RabbitMQ  
- **Deployment (future):** Docker, Kubernetes  
- **CI/CD (future):** Jenkins  

---

## Project Structure

```
prodev-ecommerce-backend/
├── src/
│   ├── core/          # Django project settings
│   ├── accounts/      # User app
│   ├── products/      # Products app
│   └── categories/    # Categories app
├── docs/
│   ├── diagrams/      # ERD and design diagrams
├── infrastructure/    # Docker, Kubernetes, CI/CD
│   ├── docker/
│   └── k8s/
├── scripts/           # Helper scripts
├── requirements.txt   # Python dependencies
└── README.md
```

---

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd prodev-ecommerce-backend/src
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate   # macOS/Linux
   env\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL database**
   Update `.env` and `settings.py` with your credentials:
   ```text
   DB_NAME=ecommerce_db
   DB_USER=postgres
   DB_PASSWORD=<your-password>
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Run initial migrations**
   ```bash
   python manage.py migrate
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Check API documentation**
   * Swagger: [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)
   * Redoc: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

---

## Database Design (ERD Placeholder)

Tables planned:

| Table                 | Description                          |
| --------------------- | ------------------------------------ |
| accounts_user         | Custom user model for authentication |
| categories_category   | Product categories                   |
| products_product      | Products catalog                     |
| products_productimage | Product images                       |

> **Note:** Full ERD diagram will be added once models are finalized.

---

## API Endpoints (Placeholder)

| Method | Endpoint                | Description                               |
| ------ | ----------------------- | ----------------------------------------- |
| POST   | /api/accounts/register/ | Register a new user                       |
| POST   | /api/accounts/login/    | Login and get JWT                         |
| GET    | /api/products/          | List products with filter, sort, paginate |
| POST   | /api/products/          | Add new product                           |
| GET    | /api/categories/        | List categories                           |
| POST   | /api/categories/        | Add new category                          |

> Endpoints will be expanded with actual paths and parameters as development progresses.

---

## Git Workflow

* **Branching:** `feature/<feature-name>` → PR → merge to `develop`
* **Commits:** Use conventional commits:
  * `feat:` new feature
  * `fix:` bug fix
  * `docs:` documentation
  * `chore:` minor updates
  * `perf:` performance improvements

---

## Future Enhancements

* JWT Authentication for users
* Celery + RabbitMQ for notifications
* Kubernetes for container orchestration
* CI/CD pipelines with Jenkins
* Unit & integration testing
* Production-ready deployment

---

## Notes

* This README serves as a **living document**, updated as the project progresses.
* ERD diagrams, API specifications, and CI/CD configuration will be added in later phases.