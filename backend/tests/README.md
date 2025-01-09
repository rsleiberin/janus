# Backend Tests

## Overview
This document outlines the **test strategy** for Janus’ backend, covering API endpoints, database interactions, utility functions, and error handling. Our approach includes **unit**, **integration**, and **end-to-end** tests to ensure the robustness and reliability of the backend components.

---

## Testing Organization and File Status

### Root
- **`README.md`**: Documentation
- **`__init__.py`**: Module Initialization
- **`conftest.py`**: ✔️ Complete
- **`test_config.py`**: ✔️ Complete

### Database (`db/`)
- **`__init__.py`**: Module Initialization
- **`test_db_schema_creation.py`**: ✔️ Complete
- **`test_db_setup.py`**: ✔️ Complete
- **`test_seed_data.py`**: ✔️ Complete

#### Helpers (`db/helpers/`)
- **`__init__.py`**: Module Initialization
- **`test_admin_helpers.py`**: ✔️ Complete
- **`test_analytics_helpers.py`**: ✔️ Complete
- **`test_image_helpers.py`**: ✔️ Complete
- **`test_log_helpers.py`**: ✔️ Complete
- **`test_multi_model_helpers.py`**: ✔️ Complete
- **`test_security_helpers.py`**: ✔️ Complete
- **`test_user_helpers.py`**: ✔️ Complete

### Extensions (`extensions/`)
- **`__init__.py`**: Module Initialization

### Routes (`routes/`)
- **`__init__.py`**: Module Initialization
- **`test_status_routes.py`**: 🚧 In Progress
- **`test_file_routes.py`**: 🚧 In Progress
- **`test_image_routes.py`**: 🚧 In Progress

### Static (`static/`)
- **`__init__.py`**: Module Initialization

### Templates (`templates/`)
- **`__init__.py`**: Module Initialization

### Utilities (`utils/`)
- **`__init__.py`**: Module Initialization
- **`test_error_handling.py`**: ✔️ Complete
- **`test_logger.py`**: ✔️ Complete

#### Error Handling (`utils/error_handling/`)
- **`api/errors.py`**: 🚧 In Progress
- **`db/test_errors.py`**: ✔️ Complete
- **`extensions/errors.py`**: 🚧 In Progress
- **`routes/errors.py`**: 🚧 In Progress
- **`test_error_handling.py`**: ✔️ Complete
- **`tests/errors.py`**: 🚧 In Progress
- **`utils/errors.py`**: 🚧 In Progress

---

## Coverage Updates

- **`utils/error_handling/error_handling.py`**: Tested and integrated with `logger.py` for centralized logging. **Complete.**
- **`utils/error_handling/db/errors.py`**: Comprehensive unit tests written to validate error handling for all error classes and functions. **Complete.**
- **Centralized Logging**: All relevant test files validate integration with `logger.py`, ensuring error handling utilizes the centralized logging system. **Complete.**
- **Routes Testing**: All route test files (`test_status_routes.py`, `test_file_routes.py`, `test_image_routes.py`) are currently marked as **In Progress**.

---

## Best Practices for Writing Tests

1. **Test Granularity**:
   - Write **unit tests** for individual functions and classes.
   - Write **integration tests** to validate interactions between components.
   - Write **end-to-end tests** for full user workflows.

2. **Fixtures**:
   - Use `conftest.py` for shared fixtures to maintain consistency and reduce duplication.
   - Leverage session and function-level fixtures for database setup and teardown.

3. **Organize by Scope**:
   - Group tests logically (e.g., `db/` for database-related tests, `routes/` for API endpoints, `utils/` for utility functions).

4. **Keep Tests Isolated**:
   - Ensure each test runs independently by resetting the environment or database state.

5. **Run Regularly**:
   - Integrate tests into CI/CD pipelines to catch issues early.

---

## Running Tests

### Prerequisites
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

   ```
2. **Install Testing Libraries**:
   ```bash
   pip install pytest pytest-flask
   ```

### Commands
- **Run All Tests**:
  ```bash
  pytest
  ```
- **Run Specific Test Files**:
  ```bash
  pytest backend/tests/<path_to_test_file>
  ```
- **Run Specific Test Functions**:
  ```bash
  pytest backend/tests/<path_to_test_file>::<test_function_name>
  ```

---

## Debugging Tips

1. **Logging**:
   - Use `pytest -s` to view print/log statements during test runs.

2. **Database Issues**:
   - Ensure the database schema is initialized before running tests.
   - Use an in-memory SQLite database for faster test execution.

3. **Path Issues**:
   - Verify the Python path is set correctly to resolve imports.

---

## Example Test Output
```plaintext
================================== test session starts ===================================
platform linux -- Python 3.8.10, pytest-8.3.4, pluggy-1.5.0
rootdir: /home/tank/janus
plugins: flask-1.3.0
collected 5 items

backend/tests/db/test_db_schema_creation.py .                                     [ 50%]
backend/tests/db/test_seed_data.py .                                              [100%]

=================================== 5 passed in 0.87s =====================================
All tests have passed successfully.
```

