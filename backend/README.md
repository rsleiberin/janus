# **Updated `backend/README.md`**

## Purpose

This directory serves as the **primary backend** for the Janus framework. Janus focuses on **user interface and experience research**, particularly analyzing images for accessibility and design token generation. The backend handles:

• **Data Management**: Storing and managing user accounts, logs, and image metadata.  
• **API Endpoints**: Offering secured routes for authentication, image operations, and administrative tasks.  
• **Integration**: Serving as the foundation for further expansions, such as design token calculations, advanced image analysis, and future front-end integrations.

---

## Overview

The backend contains everything needed for Janus’s server-side logic:

• **Routes** for user management, security, admin tasks, and image handling.  
• **Models** describing the database schema (users, images, logs, analytics).  
• **Utilities** for error handling, file operations, and logging.  
• **Tests** for validating features and preventing regressions.  
• **Migrations** (via Flask-Migrate) to handle schema evolution over time.

A modular structure keeps these components decoupled and maintainable, allowing easy integration of advanced features like real-time analytics or machine learning.

---

## Phases (Project Roadmap)

**Status: Ongoing** – A comprehensive refactor is underway to improve maintainability and best-practice adherence.

1. **Phase 1 (Completed)**  
   • Established core routes (admin, authentication, user, security, logs, images).  
   • Implemented base database models, migrations, and tests.  
   • Achieved an MVP with robust error handling and JWT-based security.

2. **Phase 2 (Completed)**  
   • Resolved all Flake8 `F401` warnings by splitting import statements.  
   • Ensured full compliance with Pylint and Black for high code quality.  
   • All tests passed, confirming no ImportErrors or major regressions.

3. **Phase 3 (Pending Review)**  
   • Introduce advanced image analysis routes and helper logic.  
   • Expand utility scripts for more modular CRUD operations.  
   • Refine performance and testing, preparing for next features.

4. **Phase 4 (Pending Review)**  
   • Integrate with a Next.js frontend (optional SSR templates, static assets).  
   • Provide expanded flows for admins and multi-tenant usage (design tokens, real-time dashboards).  
   • Focus on scalability and specialized integrations (ML modules, large-scale analytics).  
   • Optionally migrate from SQLite to a production-grade DB for high-traffic demands.

---

## Directory Structure

• **app.py** – Main Flask entry point.  
• **__init__.py** – Initializes the Flask app, sets configs, registers extensions.  
• **models.py** – SQLAlchemy models defining the database schema.  
• **api/** – *(Pending Review)*  
• **config/** – Environment-specific configurations (development, testing, production).  
• **db/** – Database logic, seeds, helpers, migrations.  
• **extensions/** – *(Pending Review)*  
• **instance/** – Local instance directory (e.g., `backend.db` file if using SQLite).  
• **migrations/** – Managed by Flask-Migrate for schema updates.  
• **routes/** – Core endpoints for user, admin, security, logs, images, etc.  
• **static/** – *(Pending Review)*  
• **templates/** – *(Pending Review)*  
• **tests/** – Unit and integration tests.  
• **uploads/** – Storage for uploaded files (images, etc.).  
• **utils/** – Utilities for error handling, logging, file management, security checks.

---

## Usage

1. **Install Dependencies**  
   Use `pip install -r requirements.txt` to ensure packages like Flask, Flask-Migrate, SQLAlchemy, and python-dotenv are installed.

2. **Set Environment Variables**  
   Examples include:  
   - FLASK_ENV=development  
   - UPLOAD_FOLDER=backend/uploads  
   - DATABASE_URL=sqlite:///backend/instance/backend.db

3. **Initialize and Migrate the DB**  
   Run `flask db upgrade` to apply existing migrations and align your local database with the current model definitions.

4. **Start the Server**  
   - `flask run`  
   or  
   - `python3 backend/app.py`

5. **Test the Application**  
   - `pytest backend/tests`

---

## Best Practices

• **Error Handling**: Centralized exceptions and handlers yield consistent JSON responses and logs.  
• **Testing**: Use pytest for comprehensive coverage across routes, models, and utilities.  
• **DB Helpers**: Most route logic calls into `backend.db.helpers` for organized and testable CRUD.  
• **Logging**: A single logger for both console and database outputs simplifies debugging.  
• **Modularity**: Each component (routes, models, utils) evolves independently for easy scalability.  
• **Code Quality**: Flake8, Black, and Pylint are integrated to maintain a consistent coding style.  
• **Separation of Concerns**: Each file or module focuses on one primary responsibility.

---

## Next Steps

1. **Address Pending Review Directories**  
   Expand `api/`, `extensions/`, `static/`, or `templates` as needs arise.

2. **Implement Advanced Features**  
   Include deeper image analysis, refining utility scripts as part of Phase 3.

3. **Frontend Integration**  
   Link with a Next.js client or SSR templates when Phase 4 begins.

4. **Scalability**  
   If usage grows, migrate from SQLite to a more robust production DB (PostgreSQL, etc.).

5. **Ongoing Code Quality**  
   Continue using Flake8, Black, Pylint, and Pytest to keep technical debt low and reliability high.

By following these guidelines and organizational patterns, the Janus backend remains flexible, allowing developers to add features or adapt to new requirements with minimal disruption.
