# backend/db/README.md

## Overview

The `db/` directory centralizes scripts, helpers, and seed data that manage Janus’s backend data. By leveraging **Flask-Migrate** for schema migrations and a modular structure for CRUD logic, this directory simplifies ongoing development, testing, and maintenance.

Key responsibilities of this directory include:
- **Database Initialization** via Flask-Migrate (e.g., `flask db upgrade`).
- **Seeding** the database with representative or test data (using the `seed_data/` folder).
- **Helper Modules** providing targeted CRUD and domain-specific operations.
- **Production-Ready** patterns for a clean, maintainable data layer.

---

## Directory Structure

backend/db/  
• `__init__.py` – Exposes the shared SQLAlchemy instance (`db`).  
• `db_setup.py` – Utility to create a Flask app with DB connectivity, relying on Alembic (no direct `create_all()` calls).  
• `seed_data.py` – Entrypoint for seeding data via domain-specific scripts.  
• `seed_data/`  
  ◦ `__init__.py` – Defines `run_all_seeds()`, orchestrating domain seeds.  
  ◦ `users_seed.py`, `images_seed.py`, `logs_seed.py`, `security_seed.py` – Scripts generating sample data for each domain.  
• `helpers/`  
  ◦ `__init__.py` – Imports all helper modules.  
  ◦ `base_crud.py` – Generic CRUD class for SQLAlchemy models.  
  ◦ `admin_helpers.py`, `analytics_helpers.py`, `image_helpers.py`, etc. – Domain modules providing specialized DB logic.  
• `migrations/`  
  ◦ (Flask-Migrate-managed files) – Apply schema changes with `flask db upgrade`.

---

## Usage and Best Practices

1. **Migrations, Not `create_all()`**  
   • Use `flask db upgrade` to keep your DB in sync with model changes.  
   • To add or remove columns, generate and apply Alembic scripts with `flask db migrate -m "..."` then `flask db upgrade`.

2. **Seeding Data**  
   • After upgrading the schema, seed sample data in a Flask shell:  
     ```
     from backend.db.seed_data import run_all_seeds
     run_all_seeds()
     ```
   • Each domain has a dedicated seed file for organization and scalability.

3. **Helper Modules**  
   • **`base_crud.py`** standardizes common methods like `create`, `get_by_id`, `update`, and `delete`.  
   • Domain-specific helpers (e.g., `analytics_helpers.py`) add more advanced logic when needed.

4. **Pending Features**  
   • `image_analysis_helpers.py` remains a placeholder for advanced image analysis logic.  
   • As the system evolves, new helper files and seed scripts can be added without disrupting existing code.

5. **Workflow**  
   • **Initialize** a Flask app context (e.g., `db_setup.py`)  
   • **Migrate** (`flask db upgrade`)  
   • **Seed** (optional)  
   • **Use** domain helpers in routes or scripts for clean, testable DB access.