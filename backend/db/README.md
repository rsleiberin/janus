# Database Directory

## Overview
This directory contains database-related scripts for the Janus project. It handles the database schema, helpers, and seed data required for the application to function properly. The database is designed to work with SQLAlchemy and SQLite (for development purposes), with future support for more scalable databases planned.

---

## Files and their Purpose

### **db/**
- **db_setup.py**: Script for setting up the database schema. It creates the necessary tables for the application to interact with, including `images` for storing metadata. **[✅ Completed | Ticket #001, #010]**
- **db_helpers.py**: Contains common database operations, such as queries and utilities for interacting with the `images` table. **[🚧 In Progress | Ticket #13]**
- **seed_data.py**: Script for populating the database with initial data, useful for testing or seeding the application with necessary content. **[🚧 In Progress | Ticket #14]**
- **db_schema_creation.py**: Refactored script to create the database schema separately from `db_setup.py`, ensuring the database creation logic is modular and reusable. **[🚧 In Progress | Ticket #15]**

---

## Database Schema

The database schema is defined using SQLAlchemy models in `models.py`. Currently, the tables include `images`, `users`, `admins`, `logs`, `analytics`, and `security`. These tables store metadata and other relevant information for the backend to function efficiently.

### Best Practices Considerations:
- **Normalization**: The schema follows normalization best practices with foreign key relationships.
- **Indexes**: For performance, especially with searches, indexes should be added on frequently queried columns, such as `email` in the `users` table and `timestamp` in the `logs` table.
- **Data Integrity**: All foreign key constraints are set up to ensure referential integrity between related tables.
- **Scalability**: The schema is designed to scale by adding more tables in a structured way, preparing for future database migrations (e.g., PostgreSQL or MySQL).

---

## Database Setup

1. **Initialization**: The database schema is set up by running `db_schema_creation.py`.
2. **Database URI**: The application is configured to use SQLite by default with the URI pointing to `instance/image_processing.db`.

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
- **Support for other databases**: The current implementation uses SQLite for simplicity and development. Future plans involve migrating to more robust systems like PostgreSQL or MySQL, as outlined in the [future issues](#).
- **Data seeding**: We'll enhance the seeding script to populate the database with more comprehensive data for testing and development.
