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
- **app.py**: Main Flask application entry point **[✅ Completed | Ticket #001]**
- **config.py**: Backend configuration settings **[🚧 In Progress | Ticket #002]**
- **models.py**: SQLAlchemy models for database schema **[✅ Completed | Ticket #003]**
- **routes/**: Modularized Flask routes
  - **image_routes.py**: Handles API requests for image-related operations **[🚧 In Progress | Ticket #004]**
  - **status_routes.py**: Provides basic health checks for monitoring **[✅ Completed | Ticket #006]**
  - **file_routes.py**: Provides routes to list and retrieve file contents **[✅ Completed | Ticket #008]**
  - **user_routes.py**: Placeholder for user-specific routes **[❌ Pending | Phase 2]**
  - **admin_routes.py**: Placeholder for admin-specific routes **[❌ Pending | Phase 3]**
  - **README.md**: Documents all routes and their functionality **[🚧 In Progress | Ticket #007]**
- **templates/**: Flask templates for rendering views **[❌ Pending | Phase 3]**
- **static/**: Static files for serving assets **[❌ Pending | Phase 3]**
- **extensions/**: Placeholder for future capabilities
  - **machine_learning.py**: ML-based functionality for advanced features **[❌ Pending | Post-MVP]**
  - **data_analytics.py**: Tools for analyzing processed data **[❌ Pending | Post-MVP]**
  - **integrations.py**: Handles third-party integrations **[❌ Pending | Phase 4]**
- **tests/**: Test cases for backend modules
  - **test_image_routes.py**: Tests for image-related API endpoints **[❌ Pending | Ticket #009]**
  - **test_status_routes.py**: Tests for status-related endpoints **[✅ Completed | Ticket #010]**
  - **test_file_routes.py**: Tests for file-related API endpoints **[✅ Completed | Ticket #011]**
  - **README.md**: Documents the testing strategy and process **[🚧 In Progress | Ticket #012]**
- **utils/**: Shared utility scripts
  - **file_handler.py**: Utility functions for file operations **[🚧 In Progress | Ticket #013]**
  - **logger.py**: Logging configuration for the backend **[🚧 In Progress | Ticket #014]**
  - **security.py**: Security utilities (e.g., input validation, sanitization) **[❌ Pending | Phase 2]**
- **db/**: Database-specific scripts and helpers
  - **db_setup.py**: Sets up the database schema **[✅ Completed | Ticket #001]**
  - **db_helpers.py**: Common database operations **[❌ Pending | Phase 2]**
  - **seed_data.py**: Script to populate the database with initial data **[❌ Pending | Phase 2]**
- **api/**: API-related extensions
  - **openapi_spec.yaml**: OpenAPI specification for documenting the API **[❌ Pending | Phase 4]**
  - **api_auth.py**: Handles API authentication **[❌ Pending | Phase 4]**
  - **api_throttling.py**: Manages API rate limiting **[❌ Pending | Phase 4]**

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

## Database Schema

The database schema is defined using SQLAlchemy models in `models.py`. Currently, the following tables are defined:

- **images**: Stores metadata for uploaded images. Contains columns like `filename`, `width`, `height`, `bit_depth`, and `image_metadata`.

- **users**: Stores user information, including `username`, `email`, and `password_hash`.

- **admins**: Stores administrative user information and their associated roles. Connected to the `users` table.

- **logs**: Stores logs of user actions, including the type of action and the associated user.

- **analytics**: Stores analytical and research data, with a `data` field of type JSON for flexible storage. This also serves as the table for storing research data with an optional `research_topic` column.

- **security**: Stores security-related actions, including user activities that are tracked for security purposes.

---

## Workflow: Development from Root Directory

### **Working Context**
All commands should be executed from the project root (`janus/`):
```bash
cd ~/janus
python3 backend/app.py

