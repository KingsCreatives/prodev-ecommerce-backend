# Documentation Overview

Welcome to the **Documentation Hub** for the **ProDev E-Commerce Backend** project.
This folder contains all architectural, design, and development reference materials used throughout the system.

---

## Folder Structure

```
docs/
│
├── diagrams/
│    ├── erd.png
│    └── (other future diagrams)
│
└── README.md   <-- (this file)
```

---

## Contents

### **1. Entity Relationship Diagram (ERD)**

A full database relationship diagram showing:

* Users
* Categories
* Cart
* Cart Items
* Products
* Product Images
* Orders
* Order Items
* Notifications

📍 Location: `docs/diagrams/erd.png`
This ERD is the single source of truth for all database structure decisions.

---

### **2. Architecture Notes (Coming Soon)**

This section will include documents describing:

* Backend architecture (Django + DRF)
* Authentication workflow (JWT)
* Asynchronous processing (Celery + RabbitMQ)
* Storage strategy for product images
* Notifications workflow (email + in-app)
* CI/CD overview (GitHub Actions + Jenkins)
* Containerization (Docker + Kubernetes)

---

### **3. API Documentation**

Full API specifications will be generated using:

* **Swagger / OpenAPI** (`/api/docs`)
* Postman Collection
  Location (planned): `docs/api/postman_collection.json`

---

### **4. System Workflows**

Documentation for core business flows, including:

* User registration & authentication
* Product creation & management
* Order lifecycle
* Stock update process
* Notification delivery (real-time & async)

---

## Tools Used for Documentation

* **Mermaid / Graphviz** — for ERD & architecture diagrams
* **Markdown** — for lightweight documentation
* **OpenAPI** — for API documentation

---

## Purpose of This Documentation

This directory exists to:

* Provide clear technical understanding for future contributors
* Support frontend development with accurate API specs
* Assist DevOps with deployment knowledge
* Serve as a reference during debugging and testing

