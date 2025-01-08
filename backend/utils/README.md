# Utils Directory

## Overview
This directory contains utility scripts for the Janus backend. These utilities provide core functionalities such as file handling, logging configuration, error handling, and security features. The directory is designed for modularity and scalability, ensuring that utility functions are reusable and easy to integrate across the backend.

---

## Directory Structure

### **utils/**
- **file_handler.py**: Utility functions for file operations **[🚧 In Progress | Ticket #30]**
- **logger.py**: Centralized logging configuration for the backend **[✅ Completed]**
- **security.py**: Security utilities (e.g., input validation, sanitization) **[🚧 In Progress | Ticket #32]**
- **error_handling/**:
  - **api/errors.py**: Error handling for API-related operations **[🚧 In Progress | Ticket #58]**
  - **db/errors.py**: Error handling for database-related operations **[🚧 In Progress | Ticket #58]**
  - **extensions/errors.py**: Error handling for extensions **[🚧 In Progress | Ticket #58]**
  - **routes/errors.py**: Error handling for routes **[🚧 In Progress | Ticket #58]**
  - **tests/errors.py**: Error handling for test cases **[🚧 In Progress | Ticket #58]**
  - **utils/errors.py**: General error handling for utilities **[🚧 In Progress | Ticket #58]**
- **README.md**: Documents the utility scripts and their functionalities **[✅ Completed | Ticket #61]**

---

## Logger Module (`logger.py`)

### Overview
The `logger.py` module provides centralized logging functionality for the backend, supporting both console and database logging. It ensures all logs are consistent, structured, and enriched with contextual metadata.

### Key Features
- **Dynamic Log Levels**:
  - Log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) can be configured dynamically during initialization or through an environment variable (`LOG_LEVEL`).
- **Flexible Output**:
  - Logs messages to the console.
  - Optionally stores logs in the database.

### Initialization
You can initialize the logger with a custom log level or rely on the environment variable `LOG_LEVEL`.

#### Example
```python
from backend.utils.logger import CentralizedLogger

# Initialize logger with dynamic log level
logger = CentralizedLogger("app_logger", log_level="INFO")

# Or rely on the environment variable
logger = CentralizedLogger("app_logger")
```

### Methods
- **`log_to_console(level, message, **kwargs)`**:
  Logs messages to the console with optional metadata.

  Example:
  ```python
  logger.log_to_console("DEBUG", "Application started", module="main")
  ```

- **`log_to_db(level, message, module=None, user_id=None, meta_data=None)`**:
  Logs messages to the database.

  Example:
  ```python
  logger.log_to_db(
      level="ERROR",
      message="Failed to connect to the database",
      module="db_setup",
      user_id=1,
      meta_data={"details": "Connection timed out"}
  )
  ```

---

## Completed Integration

### Backend Directory
- Integrated `CentralizedLogger` into:
  - `config.py` and its corresponding test `test_config.py`.
  - Added logging for validation warnings and debug-level database URI outputs.

### DB Directory
- Integrated `CentralizedLogger` into all database helper files:
  - `log_helpers.py`
  - `multi_model_helpers.py`
  - `security_helpers.py`
  - `user_helpers.py`
- Updated all related tests to mock and validate logger functionality.

---

## Remaining Integration

### Pending
- **APIs and Routes**: Logging integration will be addressed as these directories are created and populated.
- **Extensions and Other Directories**: Integration will proceed when implemented.

---

## Relevant Tickets
- **Ticket #30**: Complete `file_handler.py` **[🚧 In Progress]**
- **Ticket #32**: Implement `security.py` **[🚧 In Progress]**
- **Ticket #58**: Centralized Error Handling for `utils` Directory **[🚧 In Progress]**

