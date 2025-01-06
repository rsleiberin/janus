# Backend Directory

## Overview
This directory contains the Flask backend for the Janus project, responsible for handling API requests, database operations, and backend logic. It integrates seamlessly with the `image_processing` module and the Next.js frontend. The backend is designed to be modular, scalable, and ready for future extensions.

---

## Goals

### Current Goals (MVP)
1. Provide a modular structure for handling API routes and database operations.
2. Facilitate interaction between the frontend and backend via RESTful API endpoints.
3. Enable integration with `image_processing` scripts for metadata extraction and analysis.

### Future Goals (Post-MVP)
1. Add API authentication and security mechanisms.
2. Integrate advanced features like machine learning and data analytics.
3. Scale database operations to handle larger datasets and real-time queries.
4. Support admin and user-specific functionalities.

---

## Directory Structure with Implementation Stages

### **backend/**
- **app.py**: Main Flask application entry point **[✅ Completed]**
- **config.py**: Backend configuration settings **[✅ Completed]**
- **models.py**: SQLAlchemy models for database schema **[✅ Completed]**
- **routes/**: Modularized Flask routes **[🚧 In Progress]**
- **templates/**: Flask templates for rendering views **[❌ Pending | Phase 3]**
- **static/**: Static files for serving assets **[❌ Pending | Phase 3]**
- **extensions/**: Placeholder for future capabilities **[🚧 In Progress]**
- **tests/**: Test cases for backend modules **[✅ Completed]**
- **utils/**: Shared utility scripts **[🚧 In Progress]**
- **db/**: Database-specific scripts and helpers **[✅ Completed]**
- **migrations/**: Tracks database schema changes using Flask-Migrate **[🔄 Managed | Flask-Migrate]**
- **api/**: API-related extensions **[❌ Pending | Phase 4]**

---

## Database Schema

The database schema is defined using SQLAlchemy models in `models.py`. Below is a high-level overview of the tables:

### **images Table**
- **Purpose**: Stores metadata for uploaded images.
- **Key Columns**:
  - `id`: Unique identifier for each image.
  - `filename`: Name of the image file, must be unique.
  - `width`, `height`: Dimensions of the image.
  - `image_metadata`: Additional metadata stored in JSON format.
- **Relationships**: None.

### **users Table**
- **Purpose**: Stores user information.
- **Key Columns**:
  - `id`: Unique identifier for each user.
  - `username`: Unique username for the user.
  - `email`: Unique email address.
  - `password_hash`: Hashed password for authentication.
  - `role`: Role of the user (e.g., admin, user).
- **Relationships**: Referenced by `logs`, `admins`, and `security` tables.

### **admins Table**
- **Purpose**: Stores administrative user information.
- **Key Columns**:
  - `id`: Unique identifier for each admin.
  - `user_id`: References the user this admin entry is associated with.
  - `admin_level`: The level of admin privileges (e.g., superadmin, moderator).
- **Relationships**: Linked to `users` table via `user_id`.

### **logs Table**
- **Purpose**: Stores logs of user actions.
- **Key Columns**:
  - `id`: Unique identifier for each log entry.
  - `user_id`: References the user who performed the action.
  - `action`: Description of the action performed.
  - `module`: The system module where the action originated.
  - `level`: Log level (e.g., INFO, DEBUG).
  - `meta_data`: Additional metadata about the action (stored in JSON format).
  - `timestamp`: Timestamp of the log entry.
- **Relationships**: Linked to `users` table via `user_id`.

### **analytics Table**
- **Purpose**: Stores analytical and research data.
- **Key Columns**:
  - `id`: Unique identifier for each analytics entry.
  - `data`: JSON data containing the analytics or research information.
  - `research_topic`: Optional field for categorizing the research topic.
  - `created_at`: Timestamp for when the entry was created.
- **Relationships**: None.

### **security Table**
- **Purpose**: Tracks security-related actions for users.
- **Key Columns**:
  - `id`: Unique identifier for each security action.
  - `user_id`: References the user who triggered the security action.
  - `action`: Description of the security event.
  - `timestamp`: Timestamp of the security action.
- **Relationships**: Linked to `users` table via `user_id`.

## Managed Schemas

### **alembic_version Table**

- **Purpose**: Tracks the current state of database migrations managed by Alembic.
- **Key Columns**:
  - `version_num`: Unique identifier for the current migration applied to the database.
- **Relationships**: None (managed automatically by Alembic).


---

### **Notes on Changes**
- Added the `migrations/` directory with a new status symbol **[🔄 Managed | Flask-Migrate]**, reflecting its automatic and tool-driven nature.
- Updated the `logs` schema to include `module`, `level`, and `meta_data` fields as discussed and implemented.
- Maintained other schema details as they were confirmed to be accurate.


---

## Workflow Phases and Rationale

### **Phase 1: Core Backend Implementation (Completed)**
- Focus: Establish the foundation for the backend, including database setup, basic routing, and initial file handling utilities.
- **Completed**:
  - `app.py`: Main Flask application setup.
  - `models.py`: SQLAlchemy models for the database.
  - `db/`: Database scripts and helpers.
  - Basic route setup (`status_routes.py`, `file_routes.py`).
- **In Progress**:
  - `image_routes.py`: API for image-related operations **[🚧 In Progress | Ticket #5]**.
  - Utilities: File handler and logging utilities **[🚧 In Progress | Tickets #8, #9]**.

---

### **Phase 2: Utility Refinement and Integration**
- Focus: Finalize utility scripts, test them, and ensure consistent usage across the backend.
- **Current Goals**:
  - Finalize and test `utils/` **[🚧 In Progress | Tickets #8, #9, #30]**.
  - Ensure all existing routes and database helpers integrate with finalized utilities.
  - Begin testing for database and utility scripts **[🚧 In Progress | Ticket #40]**.
- **Pending**:
  - Security utilities (`security.py`) **[❌ Pending | Ticket #32]**.
  - User management (`user_routes.py`) **[❌ Pending | Ticket #11]**.

---

### **Phase 3: Frontend Integration and Advanced Routing**
- Focus: Add frontend rendering support and advanced routes for user and admin functionalities.
- **Planned Goals**:
  - Integrate `templates/` and `static/` directories for frontend rendering **[❌ Pending | Tickets #15, #17, #16]**.
  - Implement `admin_routes.py` and finalize `user_routes.py` **[❌ Pending | Tickets #15, #11]**.

---

### **Phase 4: Scalability and Extensions**
- Focus: Prepare the backend for advanced use cases, scalability, and external integrations.
- **Planned Goals**:
  - API enhancements:
    - API authentication **[❌ Pending | Ticket #18]**.
    - API throttling **[❌ Pending | Ticket #19]**.
    - OpenAPI documentation **[❌ Pending | Ticket #20]**.
  - Extensions:
    - Machine learning utilities **[❌ Pending | Ticket #21]**.
    - Data analytics tools **[❌ Pending | Ticket #22]**.
    - Third-party integrations **[❌ Pending | Ticket #23]**.
  - Database scalability enhancements (e.g., PostgreSQL migration) **[❌ Pending | Ticket #24]**.

---

### Updated Rationale
1. **Foundation First**: The foundational components (database, models, basic routes) are completed, providing a stable backend core.
2. **Utility Refinement**: Utilities are actively being refined and tested to standardize backend operations.
3. **Frontend Readiness**: Once utilities are stable, efforts will shift toward integrating frontend rendering capabilities and user/admin routes.
4. **Advanced Features**: Scalability, security, and advanced analytics will be addressed in later phases after core functionality is finalized.

---

## Workflow: Development from Root Directory

### **Working Context**
All commands should be executed from the project root (`janus/`):
```bash
cd ~/janus
python3 backend/app.py

