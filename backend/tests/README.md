# Backend Tests

## Overview
This document outlines the **test strategy** for Janus’ backend, covering API endpoints, database interactions, and utility functions. Our approach includes **unit**, **integration**, and **end-to-end** tests to ensure the robustness and reliability of the backend components.

---

## Testing Strategy

1. **Unit Tests**: Focus on individual components (e.g., a single helper method).  
2. **Integration Tests**: Verify the interaction between multiple components (e.g., Flask routes + Database).  
3. **End-to-End Tests**: Simulate real user workflows across the entire backend system.  

---

## Running Tests

### Prerequisites
1. **Install Dependencies**  
   - Ensure all dependencies listed in `requirements.txt` are installed using pip:
     ```
     pip install -r requirements.txt
     ```
2. **Install Additional Testing Dependencies**  
   - Ensure `pytest` and `pytest-flask` are installed:
     ```
     pip install pytest pytest-flask
     ```

### Running All Tests
Run `pytest` from the project root to execute all test cases:


### Running Specific Test Files
Provide the path to the specific test file. For example:
`pytest backend/tests/db/test_db_schema_creation.py`


### Running Specific Test Functions
Use the `::` syntax to run a specific test function. For example:
`pytest backend/tests/db/test_seed_data.py::test_create_seed_data`


---

## Testing Organization

- **`tests/`** folder under `backend/`  
- **Common Fixtures** live in `conftest.py` (session & function-level DB setup).  
- **Helpers** are tested in `test_<model>_helpers.py` files.  
- **Routes** are tested in `test_<route>_routes.py` files.  

### Example Test Files
1. **`test_db_setup.py`**  
   - **Purpose**: Verifies that `create_app` works and the DB engine is initialized correctly.  
   - **Status**: **[✅ Completed | Ticket #020]**
2. **`test_db_schema_creation.py`**  
   - **Purpose**: Checks that `db_schema_creation.py` successfully creates the schema.  
   - **Status**: **[✅ Completed | Ticket #021]**
3. **`test_seed_data.py`**  
   - **Purpose**: Confirms `seed_data.py` properly inserts initial records.  
   - **Status**: **[✅ Completed | Ticket #022]**
4. **`test_user_helpers.py`**, **`test_admin_helpers.py`**, etc.  
   - **Purpose**: Ensures CRUD logic in each helper is correct.  
   - **Status**: **[✅ Completed across multiple tickets | Tickets #023, #024, ...]**

---

## Test Fixtures

**`conftest.py`** offers:
- **`app()`** fixture: Creates a Flask app with the **in-memory** DB override.  
- **`session_db_setup`**: Validates DB connectivity once per session.  
- **`function_db_setup`**: Creates/drops tables for each test function, ensuring isolation.

### Fixture Details
- **`app`**  
  - **Scope**: `session`  
  - **Purpose**: Sets up the Flask application with a testing configuration, overriding the database URI to use an in-memory SQLite database for tests.

- **`session_db_setup`**  
  - **Scope**: `session`  
  - **Purpose**: Performs a one-time check to ensure the database connection is successful before running tests.

- **`function_db_setup`**  
  - **Scope**: `function`  
  - **Purpose**: Ensures each test function has a clean database state by creating all tables before a test and dropping them after.

---

## Test Coverage

- **Database**:  
  - `db_setup.py` and `db_schema_creation.py` are tested by `test_db_setup.py` and `test_db_schema_creation.py`.  
  - Seed data validated by `test_seed_data.py`.  
  - Helper methods tested in various `test_*_helpers.py` files.  
- **Routes**:  
  - `test_status_routes.py`, `test_file_routes.py`, `test_image_routes.py` cover essential endpoints.  
- **Utilities**:  
  - `test_utils.py` checks custom utility functions.

### Current Coverage
- **Routes**:
  - Status routes: Health check endpoint **[✅ Completed | Ticket #006]**
  - File routes: File listing and content retrieval **[✅ Completed | Ticket #007]**
  - Image routes: Image-related operations **[✅ Completed | Ticket #034]**
- **Database**:
  - Database schema validation **[✅ Completed | Ticket #010]**
  - Data seeding and helper operations **[✅ Completed | Ticket #013, Ticket #014]**
- **Utilities**:
  - File handler utilities **[✅ Completed | Ticket #030]**
  - Logging configuration tests **[✅ Completed | Ticket #031]**

### Future Coverage Goals
- **Authentication and Security Testing** **[🚧 In Progress | Ticket #032]**
- **Data Analytics and Machine Learning Workflow Validation** **[🚧 In Progress | Ticket #033]**
- **Admin and User Management Endpoints** **[🚧 In Progress | Ticket #011]**

---

## Debugging Tips

1. **Check Logging**  
   - Use `pytest -s` to see log messages during the test run.

2. **Verify Python Path**  
   - Ensure that all required directories are added to the Python path to resolve imports properly.

3. **Database Issues**  
   - Ensure the database schema is initialized before running tests.
   - If issues persist, delete the database file and recreate it or ensure the in-memory DB is correctly configured.

4. **Permissions & Paths**  
   - If using file-based DBs, confirm that the target directories exist and have appropriate permissions.

---

## Example Test Output

```plaintext
================================== test session starts ===================================
platform linux -- Python 3.8.10, pytest-8.3.4, pluggy-1.5.0
rootdir: /home/tank/janus
plugins: flask-1.3.0
collected 5 items

backend/tests/db/test_db_setup.py .                                               [ 20%]
backend/tests/db/test_db_schema_creation.py .                                     [ 40%]
backend/tests/db/test_seed_data.py .                                              [ 60%]
backend/tests/db/helpers/test_user_helpers.py .                                   [ 80%]
backend/tests/db/helpers/test_admin_helpers.py .                                  [100%]

=================================== 5 passed in 0.87s =====================================
All tests have passed successfully.
[✅ All tests completed and verified | Total: 5 Passed]```