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

## Helper Modules

### **admin_helpers.py**
- **Purpose**: Provides utility functions for managing admin-related data.
- **Details**:
  - Create, retrieve, update, and delete admin records.
  - Includes helper functions to check for the existence of an admin, count admins, and fetch admins by associated user ID.
- **Status**: Complete and verified.

### **analytics_helpers.py**
- **Purpose**: Facilitates CRUD operations and utility functions for analytics data.
- **Details**:
  - Functions to create, retrieve, update, and delete analytics entries.
  - Supports fetching recent analytics, counting entries, and checking for their existence.
- **Status**: Complete and verified.

### **image_helpers.py**
- **Purpose**: Manages operations related to image metadata stored in the database.
- **Details**:
  - Functions to create, retrieve, update, and delete image records.
  - Includes filtering and querying utilities based on attributes such as size, filename, metadata, and creation date range.
- **Status**: Complete and verified.

### **log_helpers.py**
- **Purpose**: Provides utilities for managing and querying user action logs.
- **Details**:
  - Functions to create, retrieve, and delete log entries.
  - Includes utilities to fetch recent logs, retrieve logs by user ID, and check for log existence.
- **Status**: Complete and verified.

### **multi_model_helpers.py**
- **Purpose**: Supports operations that span multiple models in the database.
- **Details**:
  - Fetch logs and security actions for a specific user.
  - Query for analytics associated with specific images.
  - Check if a user is an admin and retrieve their admin level.
  - Combine image and analytics data into a unified view.
- **Status**: Complete and verified.

### **security_helpers.py**
- **Purpose**: Manages security-related actions and logging for the database.
- **Details**:
  - Functions to create, retrieve, and delete security entries.
  - Utilities for fetching recent security actions and filtering by user ID.
- **Status**: Complete and verified.

### **user_helpers.py**
- **Purpose**: Provides CRUD operations and utility functions for user data management.
- **Details**:
  - Functions to create, retrieve, update, and delete user records.
  - Includes querying users by attributes such as email or ID.
  - Supports utility functions for checking user existence and counting users in the database.
- **Status**: Complete and verified.

---
