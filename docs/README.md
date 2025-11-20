# Documentation Overview

This directory contains all architectural, design, and development documentation for the **ProDev E-Commerce Backend** project. It serves as the central reference point for contributors, frontend developers, DevOps engineers, and reviewers.

---

## Folder Structure

```
docs/
│
├── diagrams/
│    ├── erd.png
│    └── (future diagrams)
│
├── api/
│    └── postman_collection.json
│
└── README.md
```

---

## 1. Entity Relationship Diagram (ERD)

The ERD provides a complete overview of all database entities and their relationships, including:

* Users
* Categories
* Cart and Cart Items
* Products and Product Images
* Orders and Order Items
* Addresses
* Notifications

Location: `docs/diagrams/erd.png`

The ERD is the authoritative source for all database design and relationships across the system.

---

## 2. Architecture Notes (Coming Soon)

This section will include detailed documentation on:

* Backend architecture (Django + Django REST Framework)
* Authentication and authorization workflow (JWT)
* Asynchronous processing with Celery and RabbitMQ
* File storage strategy (local and cloud)
* Notification workflow (email + in-app notifications)
* CI/CD pipeline overview (GitHub Actions + Jenkins)
* Deployment model (Docker + Kubernetes)

---

## 3. API Documentation

Complete API documentation will be available through:

* Swagger/OpenAPI documentation generated at `/api/docs/`
* Postman/Thunder Client collection

Postman collection location:
`docs/api/postman_collection.json`

---

## 4. System Workflows

This section documents major workflows within the system, including:

* User registration and authentication
* Product management flow
* Order lifecycle and status updates
* Stock tracking and adjustment
* Notification dispatch (email and in-app)

---

# Authentication and Authorization (JWT)

The backend uses **JSON Web Tokens (JWT)** for authentication.
Tokens are managed using `djangorestframework-simplejwt`.

All protected endpoints require:

```
Authorization: Bearer <access_token>
```

---

## Endpoints Overview

| Endpoint              | Method | Description                               | Auth Required |
| --------------------- | ------ | ----------------------------------------- | ------------- |
| `/api/auth/register/` | POST   | Create a new user account                 | No            |
| `/api/token/`         | POST   | Obtain access and refresh JWT tokens      | No            |
| `/api/token/refresh/` | POST   | Refresh access token                      | No            |
| `/api/auth/me/`       | GET    | Retrieve the authenticated user's profile | Yes           |

---

## Registration

**POST** `/api/auth/register/`

Request:

```json
{
  "email": "user@example.com",
  "username": "myusername",
  "password": "securepassword123"
}
```

Success response (201 Created):

```json
{
  "message": "User created successfully."
}
```
#### Password rules : It must be atleast 8 character, must not be similar to your email, it cannot be a common password and you can't use only numbers as well.
---

## Login (Obtain JWT Tokens)

**POST** `/api/token/`

Request:

```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

Response:

```json
{
  "refresh": "xxxx.yyyy.zzzz",
  "access": "aaaa.bbbb.cccc"
}
```

Use the access token on protected endpoints:

```
Authorization: Bearer <access_token>
```

---

## Refresh Token

**POST** `/api/token/refresh/`

Request:

```json
{
  "refresh": "your-refresh-token-here"
}
```

Response:

```json
{
  "access": "new-access-token"
}
```

---

## Get Current User

**GET** `/api/auth/me/`

Headers:

```
Authorization: Bearer <access_token>
```

Response:

```json
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "myusername"
}
```

---

## Permissions

### IsAdminOrReadOnly

* GET, HEAD, and OPTIONS are available to all users.
* POST, PUT, PATCH, DELETE require admin/staff privileges.

Used primarily for product and category management.

### IsAuthenticated

Default for protected endpoints.
A valid access token must be present in the `Authorization` header.

---

## JWT Settings (SimpleJWT)

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}
```

---

## Testing the Authentication Flow

Using Postman or Thunder Client:

1. Register a user
2. Log in to obtain access and refresh tokens
3. Access `/api/auth/me/` with the access token
4. Refresh the access token via `/api/token/refresh/`

---

## Postman Collection

A sample Postman collection for testing authentication endpoints is located at:

```
docs/api/postman_collection.json
```

---

## Purpose of This Documentation

This documentation exists to:

* Provide a reference for backend contributors
* Support frontend development with accurate API specifications
* Assist DevOps teams during deployment
* Serve as a reliable resource during debugging and feature development
