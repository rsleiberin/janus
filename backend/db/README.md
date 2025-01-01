# Database Directory

## Overview
This directory contains all database-related scripts and files for the Janus project. It manages the database schema creation, helper functions, and seed data. By default, the application uses **SQLite** in development mode, but we maintain patterns that allow straightforward migration to more robust databases (e.g., PostgreSQL) in the future.

---

## Files and Their Purpose

### **db_setup.py**  
- **Purpose**: Creates and configures the Flask application’s database connections using the **DevelopmentConfig** (in `config.py`).  
- **Status**: **[✅ Completed | Ticket #001, #010]**  
- **Notes**:  
  - References an **absolute path** for the SQLite file in dev.  
  - Fully tested via `test_db_setup.py`.

### **db_schema_creation.py**  
- **Purpose**: A standalone script to create the database schema. Runs `db.create_all()` within the Flask app context.  
- **Status**: **[✅ Completed | Ticket #015]**  
- **Notes**:  
  - Decouples schema creation from `db_setup.py`.  
  - Tested by `test_db_schema_creation.py`.

### **helpers/**  
- **Description**: Contains sub-modules (e.g., `admin_helpers.py`, `user_helpers.py`) that encapsulate CRUD and domain logic for each model.  
- **Status**: **[✅ Completed across multiple tickets]**  
- **Notes**:  
  - Each file is tested in dedicated `test_<model>_helpers.py` files.  

### **seed_data.py**  
- **Purpose**: Seeds the database with initial data (users, images, logs, etc.).  
- **Status**: **[✅ Completed | Ticket #014]**  
- **Notes**:  
  - Tested in `test_seed_data.py`.  
  - Typically used for local development or demo environments.

---

## Database Schema

The schema is defined in `models.py` using **SQLAlchemy**. It includes tables for:
- **`users`** (basic user info)
- **`admins`** (extended admin privileges)
- **`images`** (metadata for uploaded images)
- **`logs`** (audit logs, user actions)
- **`analytics`** (storing analytical data/research info)
- **`security`** (records of security-related actions)

### Best Practices Considerations
1. **Absolute Paths for Dev**: The dev config references an absolute path in `backend/instance/image_processing.db` to avoid `sqlite3.OperationalError`.
2. **In-Memory DB for Tests**: Our `conftest.py` fixture overrides the database URI with `sqlite:///:memory:` for faster, isolated test runs.
3. **Normalization & Indexes**: Foreign keys ensure data integrity. Indexes (e.g., on `email`, `timestamp`) speed up queries.
4. **Scalability**: Migration to PostgreSQL or MySQL is straightforward thanks to SQLAlchemy’s ORM abstractions.

---

## Database Setup

1. **Initialization**  
   - Run `db_schema_creation.py` to create all tables. This ensures a fresh schema if you are working locally in dev mode.  
2. **Seeding**  
   - Run `seed_data.py` (optionally) to populate the DB with sample data (e.g., default admin user, images).  
3. **Testing**  
   - Tests automatically use **in-memory SQLite**. When you run `pytest`, tables are created/dropped per test via the `function_db_setup` fixture.

---

## Database Schema Design

Below is a summary of core models (see `models.py` for implementation details):

- **`Image`**: Stores metadata for images (`filename`, `dimensions`, `color_type`, etc.).  
- **`User`**: Stores basic user data (`email`, `password_hash`, `role`).  
- **`Admin`**: Extends `User` for admin privileges (`admin_level`).  
- **`Log`**: Records user actions (`action`, `timestamp`).  
- **`Analytics`**: Holds research/analytical data (JSON-based).  
- **`Security`**: Documents security events (`user_id`, `action`).

### Relationships:
- **`User` : `Log`** (one-to-many)  
- **`User` : `Admin`** (one-to-one)  
- **`User` : `Security`** (one-to-many)

---

## Future Improvements
- **Migration Tools**: We may integrate Alembic or Flask-Migrate to handle more advanced schema changes.  
- **Advanced Seed Data**: Expand the default seed script for broader use cases (multi-user scenarios, more robust logs).  
- **Sharding / Partitioning**: For very large data sets, consider Postgres or MySQL with partitioning strategies.

---
