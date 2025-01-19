# Routes Directory

## Purpose

The `routes/` directory is the backbone of the Janus backend, responsible for handling all API endpoints that facilitate communication between the frontend and the database. Each route module is designed to manage a specific domain of functionality, ensuring a clear separation of concerns, maintainability, and scalability. This structure supports Janus's primary goal of conducting user interface and experience research by managing user interactions, image processing, security, and administrative tasks efficiently.

---

## Overview

This directory contains modularized Flask routes for the Janus backend. Each file handles a specific domain of API functionality, integrating standardized logging, error handling, and input validation to maintain consistency and reliability across the application.

---

## Phases (Project Roadmap)

### Status: Phase 1 MVP Completed

The Routes directory has successfully completed Phase 1 of the MVP, implementing core API routes with comprehensive testing and robust error handling. Future phases will introduce advanced functionalities and integrations to enhance the backend's capabilities.

1. **Phase 1: Core Backend Implementation (Completed)**
   - Established essential routes: authentication, user management, security, logs, and image handling.
   - Implemented database models, migrations, and foundational tests.
   - Achieved MVP with consistent error handling and JWT-based security.

2. **Phase 2: Image Analysis Integration (Planned)**
   - Develop `image_analysis_routes.py` for handling image analysis tasks.
   - Implement `image_analysis_helpers.py` to manage advanced image analysis queries.
   - Expand `seed_data.py` to include sample data for image analysis testing.
   - Enhance utility scripts to support complex CRUD operations related to image analysis.

3. **Phase 3: Frontend Integration and Advanced Features**
   - Integrate with the Next.js frontend once the `image_processing` proof of concept is validated.
   - Utilize `templates/` and `static/` directories for server-side rendering or asset management if necessary.
   - Extend user and admin functionalities to support dynamic design token generation and visualization.

4. **Phase 4: Scalability and Specialized Integrations**
   - Evaluate migrating from SQLite to a more scalable RDBMS like PostgreSQL or MySQL based on performance needs.
   - Integrate machine learning modules for enhanced image analysis and UI/UX research.
   - Implement advanced security measures, including rate-limiting and multi-factor authentication.

---

## Directory Structure with Status

- **routes/**
  - **README.md** [✅ Completed]  
    Documentation for the directory and its routes.
  - **__init__.py** [✅ Completed]  
    Initializes the `routes` module.
  - **status_routes.py** [✅ Completed]  
    General routes for health checks and system status.
  - **file_routes.py** [✅ Completed]  
    Routes for handling file uploads and management.
  - **authentication_routes.py** [✅ Completed]  
    Provides endpoints for user authentication, including registration, login, and profile retrieval.
  - **user_routes.py** [✅ Completed]  
    Manages user-related functionality (e.g., profile retrieval and updates).
  - **admin_routes.py** [✅ Completed]  
    Administrative routes for managing users and fetching system logs.
  - **analytics_routes.py** [✅ Completed]  
    Routes for creating, retrieving, and deleting analytics records.
  - **error_and_health_monitoring_routes.py** [✅ Completed]  
    Routes for error tracking and health monitoring.
  - **image_routes.py** [✅ Completed]  
    Handles image-related API operations.
  - **log_routes.py** [✅ Completed]  
    Routes for accessing and managing application logs.
  - **security_routes.py** [✅ Completed]  
    Security-related routes, including access control and permissions.
  - **image_analysis_routes.py** [❌ Pending | Phase 3]  
    Routes for advanced image analysis operations.
  - **files/** [↺ Managed]  
    Placeholder for file-related assets or configurations.

---

## Walkthrough of Routes

### **status_routes.py**
**Endpoints**:
- `/status` (GET): Returns a "healthy" status message for system monitoring.

### **file_routes.py**
**Endpoints**:
- `/upload` (POST): Handles file uploads, saving metadata to the database.
- `/files/<file_id>` (GET): Retrieves information about a specific file.
- `/files` (GET): Lists all uploaded files and their metadata.

### **authentication_routes.py**
**Endpoints**:
- `/auth/register` (POST): Allows users to register with a username, email, and password.
- `/auth/login` (POST): Authenticates users and generates JWT access and refresh tokens.
- `/auth/profile` (GET): Retrieves user profile information for authenticated users.

### **user_routes.py**
**Endpoints**:
- `/user/profile` (GET): Retrieves the profile of the authenticated user.
- `/user/profile` (PUT): Updates the profile of the authenticated user.

### **admin_routes.py**
**Endpoints**:
- `/admin/users` (GET): Fetches a list of all users.
- `/admin/users/<user_id>` (DELETE): Deletes a specific user by ID.
- `/admin/logs` (GET): Fetches the latest system logs.

### **analytics_routes.py**
**Endpoints**:
- `/analytics` (POST): Creates a new analytics entry.
- `/analytics` (GET): Retrieves all analytics records.
- `/analytics/<record_id>` (GET): Fetches a single analytics entry by ID.
- `/analytics/<record_id>` (DELETE): Deletes an analytics record by ID.

### **error_and_health_monitoring_routes.py**
**Endpoints**:
- `/health` (GET): Returns system health status.
- `/simulate-error` (POST): Simulates different types of errors for testing purposes.
- `/health/simulate-unhandled-error` (GET): Simulates an unhandled exception for testing.

### **image_routes.py**
**Endpoints**:
- `/image/upload` (POST): Uploads an image file for the authenticated user.
- `/image/<image_id>` (GET): Retrieves metadata for a specific image by ID.
- `/image/<image_id>` (DELETE): Deletes a specific image by ID if owned by the authenticated user.

### **log_routes.py**
**Endpoints**:
- `/logs/` (GET): Retrieves a list of system logs.
- `/logs/<log_id>` (GET): Retrieves a specific log entry by ID.

### **security_routes.py**
**Endpoints**:
- `/security/login` (POST): Authenticates a user and issues JWT tokens.
- `/security/logout` (POST): Logs out the current user by invalidating the token.
- `/security/refresh` (POST): Refreshes the user's access token using a refresh token.
- `/security/reset-password` (POST): Sends a password reset email to the user.
- `/security/change-password` (POST): Allows a user to change their password.
- `/security/protected` (GET): A protected route for testing JWT access.

### **image_analysis_routes.py**
**Endpoints**:
- *Pending*: To be implemented in Phase 3, managing advanced image analysis operations.

---

## Best Practices

1. **Standardized Logging**  
   Utilize the `CentralizedLogger` for all logging within routes to maintain consistency and facilitate debugging.

2. **Robust Error Handling**  
   Implement centralized error-handling utilities to ensure uniform error responses and efficient troubleshooting across all routes.

3. **Input Validation**  
   Validate all incoming data at the route level using utility functions to prevent invalid or malicious inputs.

4. **Separation of Concerns**  
   Design routes to focus on a single domain of functionality, delegating shared tasks to utilities or database helpers to enhance maintainability.

5. **Comprehensive Testing**  
   Develop and maintain thorough test cases for each route in the `tests/routes/` directory, covering both successful operations and potential failure scenarios.

