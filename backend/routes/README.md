# **Updated `backend/routes/README.md`**

## Purpose

The `routes/` directory defines the **API endpoints** for the Janus application. Each Python file corresponds to a **domain-specific** Flask blueprint, providing a logical separation of concerns (e.g., user routes vs. admin routes vs. file inspection). By keeping route definitions modular, the codebase remains **maintainable**, **scalable**, and **testable** as new features are introduced.

---

## Directory Structure

- **__init__.py** – Imports each domain route file and registers them on the main Flask app.  
- **auth_routes.py** – Registration, login, logout, JWT refresh, and password handling.  
- **admin_routes.py** – Admin-only routes for user management and log access.  
- **user_routes.py** – Retrieve or update a user’s own profile.  
- **image_routes.py** – Image upload, retrieval, deletion, with ownership checks.  
- **analytics_routes.py** – CRUD endpoints for storing and retrieving analytics data.  
- **log_routes.py** – Demonstration of system log retrieval.  
- **file_routes.py** – Offers a quick way to list or read local files (optional for dev usage).  
- **error_and_health_monitoring_routes.py** – Health checks, error simulations, and system status endpoints for diagnostics.  
- **status_routes.py** – Verifies the API’s and database’s health.  
- **image_analysis_routes.py** – *(Pending)* Future advanced image analysis endpoints.


---

## Blueprint Registration

All route files are registered as blueprints in the `__init__.py` file of this directory. For example:

    def register_blueprints(app):
        from .auth_routes import auth_bp
        from .admin_routes import admin_bp
        from .user_routes import user_bp
        ...
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(admin_bp, url_prefix="/admin")
        app.register_blueprint(user_bp, url_prefix="/user")
        ...

This approach simplifies future expansions: any new route file can define a blueprint and be added here without disrupting other parts of the code.

---

## Security and Ownership

- **JWT-Based Authentication**: Most routes are protected via a `@jwt_required()` decorator that ensures clients provide a valid JSON Web Token.  
- **Admin Enforcement**: In `admin_routes.py`, a `before_request` hook verifies that the current user is indeed an admin, referencing the `Admin` table.  
- **Ownership Checks**: In modules like `image_routes.py`, only the user who owns a resource (or an admin) may delete it. This ensures basic multi-tenant security for images or other user-generated content.

---

## Code Organization and Conventions

1. **Modular Blueprints**  
   Each file focuses on one functional domain (e.g., `auth_routes.py` for authentication). This structure scales easily as new endpoints are introduced.

2. **Centralized Error Handling**  
   Routes rely on utilities in `backend/utils/error_handling/error_handling.py` to return consistent JSON errors. This keeps the client experience uniform and simplifies troubleshooting.

3. **Logging**  
   A `CentralizedLogger` instance logs key actions (user logins, image uploads, etc.). Logs can be sent to the console or the database for auditing purposes.

4. **Line Length**  
   The codebase uses an 88-character limit, enforced by **Black** and **Flake8**. This ensures readability across all routes.

5. **Broad Exception Handling**  
   Several routes employ a general `except Exception:` to capture unforeseen errors. We disable related Pylint warnings if broad catches are intentional. For production systems, refine or remove these blocks as needed.

---

## Frequently Asked Questions

**Should I keep the `files/` subdirectory?**  
- If there are no active files or configuration assets under `routes/files/`, you can safely delete it to reduce clutter. Only retain it if you plan to store domain-specific route files or resources there later.

**Can I merge certain routes?**  
- You may unify `admin_routes.py` and `user_routes.py` if you prefer. However, we recommend preserving distinct files for clarity and permission-based logic (admin vs. regular user).

**How do I handle advanced roles?**  
- You can expand on the `Admin` check by adding a `role` or `permissions` field in the `User` model. Then verify in `before_request` or at a route level whether `current_user` meets certain role requirements.

---

## Next Steps

1. **Implement `image_analysis_routes.py`** if advanced image processing is required.  
2. **Refine Admin Checks** to support more granular roles (editor, superadmin, etc.) if needed.  
3. **Consolidate or Remove** demonstration files like `file_routes.py` if they are not used in production.  
4. **Maintain** consistent error handling and logs across all new routes or expansions.

---

**Conclusion**  
By structuring your routes in a domain-oriented fashion and leveraging best practices for JWT security, error handling, and logging, the Janus backend remains **organized**, **extensible**, and **secure**—ready for ongoing development and integrations.
