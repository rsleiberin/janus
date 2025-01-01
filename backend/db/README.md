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
## Database Schema Design

### Overview
Here we describe each model in the schema, their relationships, and their purposes. This overview provides clarity on what data is stored and how the data flows through the system. The models are defined in `models.py`.

[Insert ER Diagram or visual representation of models]

### Models

#### **Image Model** (`Image`)
- **Purpose**: Stores metadata about uploaded images.
- **Attributes**:
  - `id`: Unique identifier for the image.
  - `filename`: The name of the image file.
  - `width`: Width of the image.
  - `height`: Height of the image.
  - `bit_depth`: Bit depth of the image.
  - `color_type`: Color type of the image.
  - `compression_method`: Compression method used for the image.
  - `image_metadata`: Metadata stored as JSON.
  - `created_at`: Timestamp when the image was uploaded.
  - `updated_at`: Timestamp for the last update of the image data.
- **Relationships**:
  - None (Standalone model for image metadata).

#### **User Model** (`User`)
- **Purpose**: Stores user data for authentication and authorization.
- **Attributes**:
  - `id`: Unique identifier for the user.
  - `email`: User's email address.
  - `password`: User's hashed password.
  - `role`: Role of the user (Admin/User).
  - `created_at`: Account creation timestamp.
- **Relationships**:
  - One-to-many with `Logs`.

#### **Admin Model** (`Admin`)
- **Purpose**: Stores administrative user data with additional privileges.
- **Attributes**:
  - `id`: Unique identifier for the admin.
  - `user_id`: Foreign key linking to the `users` table.
  - `admin_level`: Level of administrative access (e.g., 'superadmin', 'moderator').
- **Relationships**:
  - One-to-one with `User` via `user_id`.

#### **Log Model** (`Log`)
- **Purpose**: Stores logs of actions taken by users (admin or otherwise).
- **Attributes**:
  - `id`: Unique identifier for the log.
  - `user_id`: References a user who created the log (foreign key to `User`).
  - `action`: The action performed (e.g., "file uploaded").
  - `timestamp`: Timestamp of the log entry.
- **Relationships**:
  - Many-to-one with `User`.

#### **Analytics Model** (`Analytics`)
- **Purpose**: Stores analytical data for backend processes or research.
- **Attributes**:
  - `id`: Unique identifier for the analytics record.
  - `data`: The actual analytical data stored as JSON.
  - `created_at`: Timestamp of when the analytics data was recorded.
- **Relationships**:
  - None (Standalone model for analytics data).

#### **Security Model** (`Security`)
- **Purpose**: Stores security-related actions taken by users.
- **Attributes**:
  - `id`: Unique identifier for the security event.
  - `user_id`: Foreign key linking to the `users` table.
  - `action`: The security action (e.g., "login attempt").
  - `timestamp`: Timestamp of the security event.
- **Relationships**:
  - One-to-many with `User`.

---

## Future Improvements
- **Migration Tools**: We may integrate Alembic or Flask-Migrate to handle more advanced schema changes.  
- **Advanced Seed Data**: Expand the default seed script for broader use cases (multi-user scenarios, more robust logs).  
- **Sharding / Partitioning**: For very large data sets, consider Postgres or MySQL with partitioning strategies.

---
