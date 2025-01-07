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
- **Ticket #9**: Refactor and Enhance `logger.py` **[Completed]**
- **Ticket #30**: Complete `file_handler.py` **[In Progress]**
- **Ticket #32**: Implement `security.py` **[In Progress]**
- **Ticket #58**: Centralized Error Handling for `utils` Directory **[In Progress]**
- **Ticket #61**: Document `utils` Directory Structure and Usage **[Completed]**
