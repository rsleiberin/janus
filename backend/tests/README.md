# Backend Tests

## Overview
This document outlines the **test strategy** for Janus’ backend, covering API endpoints, database interactions, and utility functions. Our approach includes **unit**, **integration**, and **end-to-end** tests to ensure the robustness and reliability of the backend components.

---

## Testing Organization and File Status

```
backend/tests/
├── README.md                             Documentation
├── __init__.py                           Module Initialization
├── __pycache__/                          Compiled Files
├── conftest.py                          ✔️ Complete
├── test_config.py                       ✔️ Complete
├── db/
│   ├── __init__.py                       Module Initialization
│   ├── test_db_schema_creation.py       ✔️ Complete
│   ├── test_db_setup.py                 ✔️ Complete
│   ├── test_seed_data.py                ✔️ Complete
│   ├── helpers/
│       ├── __init__.py                   Module Initialization
│       ├── test_admin_helpers.py        ✔️ Complete
│       ├── test_analytics_helpers.py    🚧 In Progress | Ticket Pending
│       ├── test_image_helpers.py        🚧 In Progress | Ticket Pending
│       ├── test_log_helpers.py          🚧 In Progress | Ticket Pending
│       ├── test_multi_model_helpers.py  🚧 In Progress | Ticket Pending
│       ├── test_security_helpers.py     🚧 In Progress | Ticket Pending
│       ├── test_user_helpers.py         ✔️ Complete
├── routes/
│   ├── __init__.py                       Module Initialization
│   ├── test_status_routes.py            ✔️ Complete
│   ├── test_file_routes.py              ✔️ Complete
│   ├── test_image_routes.py             🚧 In Progress | Ticket Pending
├── utils/
│   ├── __init__.py                       Module Initialization
│   ├── test_error_handling.py           ✔️ Complete
│   ├── test_logging.py                  🚧 In Progress | Ticket Pending
├── extensions/
│   ├── __init__.py                       Module Initialization
├── models/
│   ├── __init__.py                       Module Initialization
├── static/
│   ├── __init__.py                       Module Initialization
├── templates/
│   ├── __init__.py                       Module Initialization
```

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
   - Group tests logically (e.g., `db/` for database-related tests, `routes/` for API endpoints).

4. **Use Meaningful Names**:
   - Name test files and functions to reflect their purpose (e.g., `test_seed_data.py` for testing database seeding).

5. **Keep Tests Isolated**:
   - Ensure each test runs independently by resetting the environment or database state.

6. **Run Regularly**:
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

