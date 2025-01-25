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

### Status: Ongoing

This backend is currently undergoing a comprehensive refactor to improve code maintainability, readability, and adherence to best practices. The refactor has revealed areas needing significant architectural updates, which are being systematically addressed.

1. **Phase 1 (Completed)**
   - Established core routes (admin, authentication, user, security, logs, images).
   - Implemented database models, migrations, and foundational tests.
   - Achieved MVP with consistent error handling and JWT-based security.

2. **Phase 2 (Completed)**
   - Addressed and resolved all Flake8 `F401` warnings by separating import statements.
   - Ensured Pylint and Black pass without issues, achieving a code quality rating of 10.00/10.
   - Confirmed that all tests pass successfully without ImportErrors.

3. **Phase 3 (Pending Review)**
   - Introduce advanced image analysis (image_analysis_routes, helpers).
   - Enhance utility scripts for modular CRUD operations.
   - Refine performance and testing, laying groundwork for next-stage features.

4. **Phase 4 (Pending Review)**
   - Integrate with the Next.js frontend (optional SSR templates, static assets).
   - Offer expanded user/admin flows, e.g., multi-tenant design tokens or real-time dashboards.
   - Focus on scalability and specialized integrations (machine learning modules, large-scale analytics, or third-party APIs).
   - Optionally migrate from SQLite to a production-grade database, aligning with usage demands.

---

## Directory Structure

- **app.py**  
  Main Flask application entry point.  
  **Status:** Completed

- **__init__.py**  
  Initializes the Flask application, sets up configurations, and registers extensions.  
  **Status:** Completed

- **models.py**  
  SQLAlchemy models for defining the database schema.  
  **Status:** Pending Review

- **api/**  
  **Status:** Pending Review

- **config/**  
  **Status:** Completed  
  Manages environment-specific configurations with centralized settings and validation.

- **db/**  
  **Status:** Pending Review

- **extensions/**  
  **Status:** Pending Review

- **instance/**  
  - `backend.db`  
    **Status:** Pending Review

- **migrations/**  
  Managed by Flask-Migrate for applying/rolling back schema updates.  
  **Status:** Pending Review

- **routes/**  
  **Status:** Pending Review

- **static/**  
  **Status:** Pending Review

- **templates/**  
  **Status:** Pending Review

- **tests/**  
  **Status:** Pending Review

- **uploads/**  
  - *(Sample image files)*  
    **Status:** Pending Review

- **utils/**  
  **Status:** Pending Review

---

## Usage

1. **Install Dependencies**  
   Use `pip install -r requirements.txt` to install required packages.

2. **Environment Variables** (optional)  
   - `FLASK_ENV=development`
   - `UPLOAD_FOLDER=backend/uploads`
   - `DATABASE_URL=sqlite:///backend/instance/backend.db`

3. **Initialize the DB**  
   Run `flask db upgrade` to apply migrations (if needed).

4. **Start the Server**  
   - `flask run`  
     or  
   - `python3 backend/app.py`

5. **Test the Application**  
   - `pytest backend/tests`

---

## Best Practices and Additional Notes

- **Error Handling**: Custom exceptions and centralized handlers yield consistent JSON responses and logs.
- **Testing**: We rely on pytest for end-to-end coverage across routes, models, and utilities.
- **DB Helpers**: Routes currently handle model interactions directly. As logic expands, consider consolidating reusable queries in helpers.
- **Logging**: A centralized logger allows console and optional database logging, aiding troubleshooting and audits.
- **Modularity**: The project structure supports adding new routes or entire modules without significant refactoring, ensuring ongoing scalability.
- **Code Quality and Testing Tools**:  
  All files in the project have been processed using **Flake8**, **Black**, **Pylint**, and **Pytest** to ensure adherence to coding standards and maintain high code quality. These tools are integrated into our documentation and review system to maintain consistency and reliability throughout the codebase.
- **Separation of Concerns:**  
  Each component of the backend (routes, models, utilities, etc.) is responsible for a specific aspect of the application, promoting modularity and ease of maintenance.

---


## Next Steps

1. **Review and Update Remaining Directories:**
   - Address `Pending Review` statuses by implementing necessary features and ensuring code quality.

2. **Implement Advanced Features:**
   - Develop advanced image analysis functionalities and enhance utility scripts as outlined in Phase 3.

3. **Integrate Frontend:**
   - Plan and execute the integration with the Next.js frontend as detailed in Phase 4.

4. **Scale and Optimize:**
   - Focus on scalability, migrate to a production-grade database, and integrate specialized modules in Phase 4.

5. **Maintain Code Quality:**
   - Continue using Flake8, Black, Pylint, and Pytest to uphold high code standards.
   - Regularly update dependencies and monitor for any new code quality issues.

---

Maintaining a clean and well-organized codebase is crucial for the scalability and maintainability of your project. By adhering to best practices and promptly addressing code quality issues, you ensure that your application remains robust and accessible to all team members.

If you encounter any further issues or need assistance with other parts of your project, feel free to reach out. Let's continue optimizing your codebase together!

---
