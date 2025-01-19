# Backend Directory

---

## Purpose

The Flask application in this directory serves as the **primary backend** for the Janus framework. Janus focuses on **user interface and experience research**, particularly analyzing images for accessibility and design token generation. The backend handles:

- **Data Management**: Storing and managing user accounts, logs, and image metadata.  
- **API Endpoints**: Offering secured routes for authentication, image operations, and administrative tasks.  
- **Integration**: Serving as the foundation for further expansions, such as design token calculations, advanced image analysis, and future front-end integrations.

---

## Overview

This directory contains all backend-related components for Janus, including:

- **Routes** for user management, security, admin tasks, image handling, and more.
- **Models** describing the database schema (e.g., users, images, logs, analytics).
- **Utilities** for error handling, file operations, and logging.
- **Tests** ensuring stable, predictable behavior across all core functionalities.
- **Migrations** (managed by Flask-Migrate) to track schema changes and streamline updates.

Through a modular structure, the backend is easily extensible for advanced functionalities like machine learning, real-time data analytics, or future design token expansions.

---

## Phases (Project Roadmap)

### Status: Phase 1 MVP Completed

This backend has successfully reached MVP status, implementing core routes and database models with comprehensive testing and error handling. Additional features and advanced integrations will follow in subsequent phases.

1. **Phase 1 (Completed)**  
   - Established core routes (admin, authentication, user, security, logs, images).  
   - Implemented database models, migrations, and foundational tests.  
   - Achieved MVP with consistent error handling and JWT-based security.

2. **Phase 2**  
   - Introduce advanced image analysis (image_analysis_routes, helpers).  
   - Enhance utility scripts for modular CRUD operations.  
   - Refine performance and testing, laying groundwork for next-stage features.

3. **Phase 3**  
   - Integrate with the Next.js frontend (optional SSR templates, static assets).  
   - Offer expanded user/admin flows, e.g., multi-tenant design tokens or real-time dashboards.

4. **Phase 4**  
   - Focus on scalability and specialized integrations (machine learning modules, large-scale analytics, or third-party APIs).  
   - Optionally migrate from SQLite to a production-grade database, aligning with usage demands.

---

## Directory Structure

- **app.py**  
  Main Flask application entry point (completed).

- **config.py**  
  Centralized configuration settings (completed).

- **models.py**  
  SQLAlchemy models for defining the database schema (completed).

- **routes/**  
  - admin_routes.py (completed)  
  - authentication_routes.py (completed)  
  - user_routes.py (completed)  
  - security_routes.py (completed)  
  - log_routes.py (completed)  
  - image_routes.py (completed)  
  - image_analysis_routes.py (pending)  

- **utils/**  
  Utility scripts (completed except for any image_analysis-specific needs).

- **db/**  
  Database scripts/helpers (completed except for image_analysis_helpers, pending).

- **migrations/**  
  Managed by Flask-Migrate for applying/rolling back schema updates.

- **tests/**  
  Test suites covering each route and utility (completed except for planned image_analysis tests).

- **templates/** and **static/**  
  Placeholder directories if server-side rendering or asset management is needed in later phases (phase 3).

- **extensions/**  
  Reserved for advanced or external integrations (future).

---

## Usage

- **Install Dependencies**  
  Use `pip install -r requirements.txt` to install required packages.

- **Environment Variables** (optional)  
  - `FLASK_ENV=development`  
  - `UPLOAD_FOLDER=backend/uploads`  
  - `DATABASE_URL=sqlite:///backend/instance/backend.db`  

- **Initialize the DB**  
  Run `flask db upgrade` to apply migrations (if needed).

- **Start the Server**  
  - `flask run`  
  or  
  - `python3 backend/app.py`

- **Test the Application**  
  - `pytest backend/tests`

---

## Best Practices and Additional Notes

- **Error Handling**: Custom exceptions and centralized handlers yield consistent JSON responses and logs.
- **Testing**: We rely on pytest for end-to-end coverage across routes, models, and utilities.
- **DB Helpers**: Routes currently handle model interactions directly. As logic expands, consider consolidating reusable queries in helpers.
- **Logging**: A centralized logger allows console and optional database logging, aiding troubleshooting and audits.
- **Modularity**: The project structure supports adding new routes or entire modules without significant refactoring, ensuring ongoing scalability.

---
