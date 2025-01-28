# backend/README.md

**Purpose**  
This directory contains all server-side logic for the Janus project, focusing on user accounts, logs, and image metadata. It exposes secure routes for authentication, image handling, and administrative tasks, with a modular structure for easy feature addition (e.g., advanced analytics or machine learning).  

**Overview**  
- **Routes**: Endpoints for user, admin, logs, security, images, etc.  
- **Models**: Database schema definitions.  
- **Config**: Environment-based settings (development, testing, production).  
- **DB**: Database setup, seeds, and helpers.  
- **Extensions**: Optional add-ons (analytics, integrations).  
- **Migrations**: Schema changes via Flask-Migrate.  
- **Utils**: Logging, file handling, security, and error handling.  
- **Static / Templates**: For serving static assets and HTML templates if needed.  
- **Uploads**: Where user-uploaded images are stored by default.

**Phases / Roadmap**  
1. Core routes, models, migrations, and basic tests (completed).  
2. Code linting, formatting with Flake8, Black, and Pylint (completed).  
3. Expand image analysis features and performance improvements (in progress).  
4. Integrate with a potential Next.js frontend and focus on scalability (pending).

**Usage**  
1. Install dependencies with `pip install -r requirements.txt`.  
2. Set environment variables such as `FLASK_ENV=development` or `DATABASE_URL=...`.  
3. Run `flask db upgrade` to align your DB with the current schema.  
4. Start the server with `flask run` or `python3 backend/app.py`.  
5. Use `pytest` from the repository root to run tests.

**Best Practices**  
- Centralized error handling and logging.  
- Comprehensive tests (unit, integration).  
- Code quality enforced via Flake8, Black, and Pylint.  
- Separate concerns between routes, models, and utilities.  
- Maintain a single source of truth for environment-specific configs.

---

# backend/api/README.md

**Purpose**  
Contains modules that define API-specific functionality such as custom authentication methods, rate limiting, and OpenAPI specifications.

**Key Files**  
- `api_auth.py`: Authorization helpers or decorators.  
- `api_throttling.py`: Rate limiting definitions and checks.  
- `openapi_spec.yaml`: OpenAPI spec for documentation and client generation.

**Notes**  
- Future expansions might add specialized API endpoints or blueprint structures here.  
- Adheres to the main application’s configuration and uses the same logger and error handling patterns.

---

# backend/config/README.md

**Purpose**  
Holds environment-based configuration files. Each config class inherits from a common base to ensure consistent defaults (e.g., secret keys, DB URLs).

**Key Files**  
- `base.py`: Shared settings.  
- `development.py`: Development-specific overrides.  
- `testing.py`: Testing environment overrides (in-memory DB, etc.).  
- `production.py`: Production-oriented settings (security hardening, etc.).

**Usage**  
- `config_by_name` in `__init__.py` maps environment names to these classes.  
- Provides easy toggling of environment using the `FLASK_ENV` or a custom variable.

---

# backend/db/README.md

**Purpose**  
Central location for database initialization, migrations, and seeding logic.

**Key Files & Folders**  
- `db_setup.py`: Prepares SQLAlchemy connections.  
- `seed_data.py`: Hooks for populating initial data.  
- `helpers/`: Common CRUD and utility functions for DB operations.  
- `seeds/`: Individual seed files for various data sets (users, logs, images).

**Notes**  
- Use `flask db upgrade` to apply migrations.  
- Example seeds are included for reference and can be adapted for real data.

---

# backend/db/helpers/README.md

**Purpose**  
Contains Python modules that help with specific database tasks (CRUD operations, specialized queries, data transformations).

**Highlights**  
- `admin_helpers.py`, `analytics_helpers.py`, `log_helpers.py`, etc. provide targeted utility functions.  
- Encourages clean separation from routes or models, reducing duplication.

**Usage**  
- Import these helpers in your route handlers or services to keep endpoint logic concise.  
- Shared across multiple modules for consistent database interaction patterns.

---

# backend/db/seeds/README.md

**Purpose**  
Stores individual seed files for populating the database with starter or demo data.

**Files**  
- Each file (e.g., `users_seed.py`, `logs_seed.py`) initializes a specific dataset or table.  
- A `base_seed.py` can hold shared logic (like generating random user credentials).

**Usage**  
- Called by `seed_data.py` or another orchestrator script.  
- Facilitates quick environment setup or local testing with reproducible data sets.

---

# backend/extensions/README.md

**Purpose**  
Houses optional or external integrations that can be plugged into the Flask application for extra functionality (data analytics, ML models, etc.).

**Key Files**  
- `data_analytics.py`: Might integrate with third-party services or libraries.  
- `integrations.py`: Placeholder for external APIs or OAuth.  
- `machine_learning.py`: Model loading or inference routines.

**Note**  
- These modules are not strictly required but can be enabled or disabled based on project needs.

---

# backend/migrations/README.md

**Purpose**  
Contains migration scripts generated by Flask-Migrate to track schema changes over time.

**Files & Folders**  
- `alembic.ini`: Alembic configuration file.  
- `env.py`, `script.py.mako`: Underlying Alembic code that handles migrations.  
- `versions/`: Auto-generated or custom migration scripts.

**Usage**  
- Use `flask db migrate` and `flask db upgrade` to create and apply new migrations.  
- Essential for evolving the database schema without losing data.

---

# backend/models/README.md

**Purpose**  
Holds SQLAlchemy model classes that map directly to database tables (Users, Admins, Logs, Images, etc.).

**Highlights**  
- `base.py`: May include a BaseModel class or shared columns.  
- Separate files like `user.py`, `log.py`, `analytics.py` each define logical groupings.  
- Follows best practices for relational modeling and includes relevant relationships, indexes, and constraints.

**Note**  
- Typically imported into `db_setup.py` or used directly by route controllers and helper modules.

---

# backend/routes/README.md

**Purpose**  
Defines blueprint-based routes for various feature sets (authentication, analytics, image uploads, etc.).

**Key Files**  
- `admin_routes.py`, `user_routes.py`, `log_routes.py`, etc. each handle distinct logic.  
- `register_blueprints` is likely managed in `__init__.py` (in `backend/routes/`), which the main Flask app imports.

**Best Practices**  
- Keep routes light on logic by deferring to helpers or service functions.  
- Enforce security (JWT checks, roles) at the route or blueprint level.

---

# backend/static/README.md

**Purpose**  
Reserved for static files (images, CSS, JavaScript) that the Flask app may serve directly.

**Notes**  
- `.gitkeep` ensures version control for an otherwise empty directory.  
- Usually minimal usage if a dedicated frontend handles static assets, but can be used for quick prototypes or fallback assets.

---

# backend/templates/README.md

**Purpose**  
Stores Jinja2 or related templates if server-side rendering is ever required.

**Notes**  
- `.gitkeep` ensures we track the directory in version control.  
- Typically used for simple forms or admin dashboards, or if Janus is partially SSR-based.

---

# backend/uploads/README.md

**Purpose**  
Houses user-uploaded files (images, attachments, etc.). By default, the Flask config points here for file uploads.

**Notes**  
- Structured subfolders like `user_<id>` or `user_<username>` keep files organized.  
- When scaling in production, consider external storage (S3, etc.) to offload large or frequent files.

---

# backend/utils/README.md

**Purpose**  
Contains general utility modules (logging, security checks, file handling). These are reused by routes, models, or other modules.

**Key Files**  
- `logger.py`: Centralized logging utility.  
- `file_handler.py`: Common file upload/download logic.  
- `security.py`: Extra checks or encryption routines.  
- `code_quality.py`: May hold custom linting or style-check logic if relevant.

**Notes**  
- Kept separate to avoid bloating main route or model files.  
- Conforms to the application’s overall best practices for modular, testable code.

---

# backend/utils/error_handling/README.md

**Purpose**  
Encapsulates error-handling logic and custom exceptions for consistent responses across the API.

**Highlights**  
- `error_handling.py`: Central error handler logic and utility methods.  
- `exceptions.py`: Defines custom exceptions that other parts of the app can raise.

**Usage**  
- Imported and registered in the main `create_app` factory to standardize JSON error responses.  
- Ensures that unexpected exceptions are logged properly while also returning user-friendly messages.
