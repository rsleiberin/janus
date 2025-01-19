# Database Directory

## Overview

The `db/` directory centralizes scripts and helpers that manage Janus’s data. It ensures consistent schema handling (via Flask-Migrate), provides seed data for testing and development, and offers helper modules for more complex database operations. This structure keeps database logic organized and flexible, simplifying future additions like image analysis, advanced logging, or analytics.

---

## Directory Structure with Implementation Stages

### **backend/db/**
- **README.md**: Documentation
- **\_\_init\_\_.py**: Module initialization
- **db_schema_creation.py**: Handles schema creation **[Completed]**
- **db_setup.py**: Configures database connections **[Completed]**
- **seed_data.py**: Seeds the database with initial data **[Completed]**
- **helpers/**: Contains helper modules for database operations
  - **admin_helpers.py**: Admin-specific logic **[Completed]**
  - **analytics_helpers.py**: Analytics-related utilities **[Completed]**
  - **image_helpers.py**: Image-related utilities **[Completed]**
  - **log_helpers.py**: Log-related utilities **[Completed]**
  - **multi_model_helpers.py**: Cross-model operations **[Completed]**
  - **security_helpers.py**: Security-related utilities **[Completed]**
  - **user_helpers.py**: User-related utilities **[Completed]**
  - **image_analysis_helpers.py**: Advanced image analysis queries.**[Pending]**
- **migrations/**: Auto-managed folder for Alembic migrations **[Managed]**

---

## Database Schema

The database schema is defined in `models.py`. Below is a detailed description of each table, its columns, and relationships.

### **images**
| Column              | Type         | Attributes                      | Description                                 |
|---------------------|--------------|----------------------------------|---------------------------------------------|
| `id`                | Integer      | Primary Key, Autoincrement       | Unique identifier for each image.           |
| `filename`          | String(255)  | Unique, Not Null, Indexed        | Name of the uploaded image.                 |
| `user_id`           | Integer      | Foreign Key: `users.id`          | References the user who uploaded the image. |
| `width`             | Integer      | Nullable                        | Width of the image.                         |
| `height`            | Integer      | Nullable                        | Height of the image.                        |
| `bit_depth`         | Integer      | Nullable                        | Bit depth of the image.                     |
| `color_type`        | String(50)   | Nullable                        | Type of color encoding in the image.        |
| `compression_method`| String(50)   | Nullable                        | Compression method used for the image.      |
| `image_metadata`    | JSON         | Nullable                        | JSON field to store additional metadata.    |
| `created_at`        | DateTime     | Default: `datetime.utcnow`       | Timestamp when the image was added.         |
| `updated_at`        | DateTime     | Updated on change               | Timestamp when the image was last updated.  |

---

### **image_analysis**
| Column              | Type         | Attributes                      | Description                                 |
|---------------------|--------------|----------------------------------|---------------------------------------------|
| `id`                | Integer      | Primary Key, Autoincrement       | Unique identifier for each analysis entry.  |
| `image_id`          | Integer      | Foreign Key: `images.id`         | References the associated image.            |
| `analysis_results`  | JSON         | Not Null                        | JSON data containing the analysis results.  |
| `created_at`        | DateTime     | Default: `datetime.utcnow`       | Timestamp when the analysis was created.    |
| `updated_at`        | DateTime     | Updated on change               | Timestamp when the analysis was last updated.|

---

### **users**
| Column          | Type         | Attributes                 | Description                              |
|-----------------|--------------|----------------------------|------------------------------------------|
| `id`            | Integer      | Primary Key, Autoincrement | Unique identifier for each user.         |
| `username`      | String(255)  | Unique, Not Null           | Username for the user.                   |
| `email`         | String(255)  | Unique, Not Null           | Email address of the user.               |
| `password_hash` | String(255)  | Not Null                  | Encrypted password of the user.          |

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
| `updated_at` | DateTime     | Updated on change          | Timestamp when the log was last updated. |
| `module`     | String(100)  | Nullable                  | Module name where the log originated.    |
| `level`      | String(50)   | Nullable                  | Log level (e.g., INFO, DEBUG).           |
| `log_metadata`| JSON        | Nullable                  | Additional metadata in JSON format.      |

---

### **analytics**
| Column           | Type         | Attributes                 | Description                              |
|------------------|--------------|----------------------------|------------------------------------------|
| `id`             | Integer      | Primary Key, Autoincrement | Unique identifier for each entry.        |
| `data`           | JSON         | Not Null                  | JSON field to store analytical data.     |
| `research_topic` | String(255)  | Nullable                  | Optional field for categorizing topics.  |
| `created_at`     | DateTime     | Default: `datetime.utcnow` | Timestamp when the record was created.   |
| `updated_at`     | DateTime     | Updated on change          | Timestamp when the record was last updated.|

---

### **security**
| Column       | Type         | Attributes                 | Description                              |
|--------------|--------------|----------------------------|------------------------------------------|
| `id`         | Integer      | Primary Key, Autoincrement | Unique identifier for each event.        |
| `user_id`    | Integer      | Foreign Key: `users.id`    | Links to the `users` table.              |
| `action`     | String(255)  | Not Null                  | Description of the security event.       |
| `timestamp`  | DateTime     | Default: `datetime.utcnow` | Time the event was recorded.             |
| `updated_at` | DateTime     | Updated on change          | Timestamp when the event was last updated.|

---

## Managed Tables

### **alembic_version**
| Column       | Type      | Attributes   | Description                                    |
|--------------|-----------|--------------|------------------------------------------------|
| `version_num`| String(32)| Primary Key  | Tracks the current state of database migrations.|

