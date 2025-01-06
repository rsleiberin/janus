# Database Directory

## Overview
The `db/` directory contains all database-related scripts and files for the Janus project. It handles schema creation, helper functions, seed data, and database configuration. By default, SQLite is used for development, with support for scaling to more robust databases such as PostgreSQL.

---

## Directory Structure with Implementation Stages

### **backend/db/**
- **README.md**: Documentation
- **\_\_init\_\_.py**: Module initialization
- **db_schema_creation.py**: Handles schema creation **[✅ Completed]**
- **db_setup.py**: Configures database connections **[✅ Completed]**
- **seed_data.py**: Seeds the database with initial data **[✅ Completed]**
- **helpers/**: Contains helper modules for database operations
  - **admin_helpers.py**: Admin-specific logic **[✅ Completed]**
  - **analytics_helpers.py**: Analytics-related utilities **[✅ Completed]**
  - **image_helpers.py**: Image-related utilities **[✅ Completed]**
  - **log_helpers.py**: Log-related utilities **[✅ Completed]**
  - **multi_model_helpers.py**: Cross-model operations **[✅ Completed]**
  - **security_helpers.py**: Security-related utilities **[✅ Completed]**
  - **user_helpers.py**: User-related utilities **[✅ Completed]**
- **migrations/**: Auto-managed folder for Alembic migrations **[↺ Managed]**

---

## Files and Their Purpose

### **db_schema_creation.py**
- **Purpose**: Creates the database schema by initializing all tables defined in `models.py`.
- **Details**:
  - Uses the Flask app context to call `db.create_all()`.
  - Logs the creation process and lists all tables in the database for debugging.
- **Status**: Complete and verified.

### **db_setup.py**
- **Purpose**: Configures and initializes the database connection for the Flask app.
- **Details**:
  - Uses `DevelopmentConfig` for the database URI during development.
  - Ensures the SQLite database file is created and reports its path and size in logs.
- **Status**: Complete and verified.

### **seed_data.py**
- **Purpose**: Seeds the database with initial data, such as users, images, and logs.
- **Details**:
  - Adds default admin and user accounts.
  - Creates sample images with metadata.
  - Logs user actions and security events.
  - Populates analytics data with JSON-based structures.
- **Status**: Complete and verified.

---

## Database Schema

The database schema is defined in `models.py`. Below is a detailed description of each table, its columns, and relationships.

### **images**
| Column             | Type         | Attributes                      | Description                                 |
|--------------------|--------------|----------------------------------|---------------------------------------------|
| `id`               | Integer      | Primary Key, Autoincrement       | Unique identifier for each image.           |
| `filename`         | String(255)  | Unique, Not Null, Indexed        | Name of the uploaded image.                 |
| `width`            | Integer      | Not Null                        | Width of the image.                         |
| `height`           | Integer      | Not Null                        | Height of the image.                        |
| `bit_depth`        | Integer      | Nullable                        | Bit depth of the image.                     |
| `color_type`       | String(50)   | Nullable                        | Type of color encoding in the image.        |
| `compression_method`| String(50) | Nullable                        | Compression method used for the image.      |
| `image_metadata`   | JSON         | Nullable                        | JSON field to store additional metadata.    |
| `created_at`       | DateTime     | Default: `datetime.utcnow`       | Timestamp when the image was added.         |
| `updated_at`       | DateTime     | Updated on change               | Timestamp when the image was last updated.  |

---

### **users**
| Column         | Type         | Attributes                 | Description                              |
|----------------|--------------|----------------------------|------------------------------------------|
| `id`           | Integer      | Primary Key, Autoincrement | Unique identifier for each user.         |
| `username`     | String(255)  | Unique, Not Null           | Username for the user.                   |
| `email`        | String(255)  | Unique, Not Null           | Email address of the user.               |
| `password_hash`| String(255)  | Not Null                  | Encrypted password of the user.          |
| `role`         | String(50)   | Not Null                  | Role of the user (e.g., 'admin', 'user').|

---

### **admins**
| Column        | Type         | Attributes                 | Description                              |
|---------------|--------------|----------------------------|------------------------------------------|
| `id`          | Integer      | Primary Key, Autoincrement | Unique identifier for each admin entry.  |
| `user_id`     | Integer      | Foreign Key: `users.id`    | Links to the `users` table.              |
| `admin_level` | String(50)   | Not Null                  | Level of administrative privileges.      |

---

### **logs**
| Column       | Type         | Attributes                 | Description                              |
|--------------|--------------|----------------------------|------------------------------------------|
| `id`         | Integer      | Primary Key, Autoincrement | Unique identifier for each log entry.    |
| `action`     | String(255)  | Not Null                  | Description of the logged action.        |
| `user_id`    | Integer      | Foreign Key: `users.id`    | Links to the `users` table.              |
| `timestamp`  | DateTime     | Default: `datetime.utcnow` | Timestamp when the log was created.      |
| `module`     | String(100)  | Nullable                  | Module name where the log originated.    |
| `level`      | String(50)   | Nullable                  | Log level (e.g., INFO, DEBUG).           |
| `meta_data`  | JSON         | Nullable                  | Additional metadata in JSON format.      |

---

### **analytics**
| Column           | Type         | Attributes                 | Description                              |
|------------------|--------------|----------------------------|------------------------------------------|
| `id`             | Integer      | Primary Key, Autoincrement | Unique identifier for each entry.        |
| `data`           | JSON         | Not Null                  | JSON field to store analytical data.     |
| `research_topic` | String(255)  | Nullable                  | Optional field for categorizing topics.  |
| `created_at`     | DateTime     | Default: `datetime.utcnow` | Timestamp when the record was created.   |

---

### **security**
| Column       | Type         | Attributes                 | Description                              |
|--------------|--------------|----------------------------|------------------------------------------|
| `id`         | Integer      | Primary Key, Autoincrement | Unique identifier for each event.        |
| `user_id`    | Integer      | Foreign Key: `users.id`    | Links to the `users` table.              |
| `action`     | String(255)  | Not Null                  | Description of the security event.       |
| `timestamp`  | DateTime     | Default: `datetime.utcnow` | Time the event was recorded.             |

---

### **alembic_version**
| Column       | Type      | Attributes   | Description                                    |
|--------------|-----------|--------------|------------------------------------------------|
| `version_num`| String(32)| Primary Key  | Tracks the current state of database migrations.|

---

This format makes the schema highly readable and useful for contributors. It emphasizes professionalism and adheres to documentation best practices.
