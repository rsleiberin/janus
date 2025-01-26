# backend/README.md

## Purpose

This directory serves as the **primary backend** for the Janus framework, focusing on **user interface and experience research** with image analysis for accessibility and design token generation. The backend manages:

• **Data Management**: Storing and handling user accounts, logs, and image metadata.  
• **API Endpoints**: Secured routes for authentication, image operations, and administrative tasks.  
• **Integration**: A foundation for expansions like design token calculations, advanced image analysis, and future front-end integrations.

---
## Overview

The backend contains all server-side functionality for Janus:

• **Routes** for user, security, admin, images, and more.  
• **Models** describing the DB schema (users, images, logs, etc.).  
• **Utilities** for error handling, file ops, and logging.  
• **Tests** to ensure stability across core features.  
• **Migrations** managed by Flask-Migrate, ensuring easy schema updates.

Through a modular structure, this backend supports advanced features like real-time analytics, machine learning, or custom design tokens with minimal disruption.

---
## Phases (Project Roadmap)

**Status: Ongoing** – The codebase is in a major refactor to improve maintainability and best practices.

1. **Phase 1 (Completed)**  
   - Established core routes (admin, authentication, user, security, logs, images).  
   - Implemented base models, migrations, and tests.  
   - Achieved an MVP with error handling and JWT-based security.

2. **Phase 2 (Completed)**  
   - Resolved Flake8 `F401` warnings by adjusting imports.  
   - Ensured code passes Pylint and Black, achieving high quality.  
   - Verified tests pass with no ImportErrors.

3. **Phase 3 (Pending Review)**  
   - Introduce image analysis routes and helpers.  
   - Expand modular CRUD utility scripts.  
   - Optimize performance and testing before advanced features.

4. **Phase 4 (Pending Review)**  
   - Integrate with Next.js (optional SSR and static assets).  
   - Expand user/admin flows (multi-tenant design tokens, real-time dashboards).  
   - Emphasize scalability (possible DB migration from SQLite to production-grade).  
   - Specialized integrations (ML modules, large-scale analytics, third-party APIs).

---
## Directory Structure

• `app.py` – Main Flask entry point.  
• `__init__.py` – Initializes and configures the Flask app.  
• `models.py` – Defines SQLAlchemy models for the DB.  
• `api/` – *(Pending Review)*  
• `config/` – Environment-based configurations (dev, testing, prod).  
• `db/` – DB logic, migrations, seeds, and helper modules.  
• `extensions/` – *(Pending Review)*  
• `instance/` – Local instance folder (e.g. `backend.db` if using SQLite).  
• `migrations/` – Alembic/Flask-Migrate for schema updates.  
• `routes/` – Core endpoints (user, admin, security, images, logs, etc.).  
• `static/` – *(Pending Review)*  
• `templates/` – *(Pending Review)*  
• `tests/` – Unit and integration tests.  
• `uploads/` – Storage for uploaded or processed files.  
• `utils/` – Utilities (logging, file handling, error management).

---
## Usage

1. **Install Dependencies**  
   e.g. `pip install -r requirements.txt`.  
   Include Flask, SQLAlchemy, Flask-Migrate, and any additional libraries (flask-jwt-extended, etc.).

2. **Environment Variables**  
   - `FLASK_ENV=development`  
   - `UPLOAD_FOLDER=backend/uploads`  
   - `DATABASE_URL=sqlite:///backend/instance/backend.db`

3. **Initialize & Migrate**  
   Use `flask db upgrade` to apply migrations and sync the DB schema.

4. **Start the Server**  
   - `flask run`  
   or  
   - `python3 backend/app.py`

5. **Test the Application**  
   Run `pytest backend/tests` for validation of core features.

---
## Best Practices

• **Error Handling**: Centralized exceptions and handlers in `utils/` for consistent logging and responses.  
• **Testing**: Rely on pytest for end-to-end coverage (models, routes, utilities).  
• **DB Helpers**: Routes delegate data operations to `backend.db.helpers`, reducing logic duplication.  
• **Logging**: A centralized logger captures events and issues, simplifying audits.  
• **Modularity**: Features expand easily via new routes or helper modules without large refactors.  
• **Code Quality**: Flake8, Black, Pylint, and Pytest maintain high standards throughout development.  
• **Separation of Concerns**: Each file or module focuses on a single responsibility.

---
## Next Steps

1. **Address Pending Review Directories**  
   Expand or refine `api/`, `extensions/`, `static/`, and `templates`.

2. **Advanced Features**  
   Implement deeper image analysis, refine utility scripts, or integrate machine learning modules.

3. **Frontend Integration**  
   Align with Next.js (Phase 4) for SSR or advanced user flows.

4. **Scalability**  
   Optionally migrate from SQLite to a production-grade DB. Explore caching, load balancing, or more advanced analytics.

5. **Continuous Quality**  
   Regularly run Flake8, Black, Pylint, and Pytest. Address new warnings or issues promptly to avoid technical debt.

By maintaining a structured, modular codebase, the Janus backend remains flexible and scalable, accommodating evolving features with minimal disruptions.
