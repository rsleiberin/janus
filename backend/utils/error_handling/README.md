# Utils Directory

## Overview
The `utils` directory provides shared utility scripts for the Janus backend, facilitating core operations such as file handling, security checks, logging, and error management.

---

## Directory Structure

**utils/**
- **file_handler.py** [✅ Completed]  
  Provides an API for reading, writing, and deleting files with robust error handling.
- **logger.py** [✅ Completed]  
  Centralized logging system (`CentralizedLogger`) for console and database logging.
- **security.py** [✅ Completed]  
  Handles authentication, authorization, input validation, and sanitization.
- **errors.py** [✅ Completed]  
  Utility-specific exceptions (e.g., `FileHandlerError`, `SecurityError`).
- **error_handling/**  
  - **api/errors.py** [🚧 In Progress | #Pending]  
    Handles API-specific errors, such as invalid requests or authentication issues.
  - **db/errors.py** [✅ Completed]  
    Manages database errors, including connection failures and schema violations.
  - **extensions/errors.py** [🚧 In Progress | #Pending]  
    Handles errors related to third-party integrations or extensions.
  - **routes/errors.py** [🚧 In Progress | #72]  
    Manages route-level errors, such as missing endpoints or invalid parameters.
  - **tests/errors.py** [🚧 In Progress | #Pending]  
    Provides error-handling utilities for test scenarios.
  - **utils/errors.py** [✅ Completed]  
    General-purpose error handling for utility modules.
  - **error_handling.py** [✅ Completed]  
    Defines functions for centralized error logging and formatting.

---

## Best Practices
1. **Centralized Logging**: Use `CentralizedLogger` for all logging to maintain consistency and enable database logging.  
2. **Modularity**: Each utility file should focus on a single responsibility (e.g., file operations, security logic).  
3. **Error Handling**: Wrap critical operations with `error_context` for consistent error logging and response formatting.  
4. **Testing**: Each utility file must have corresponding tests in `backend/tests/utils/`.

---

## Future Enhancements
- **Enhanced Security**: Introduce policy-based authorization and advanced sanitization.  
- **Extended File Handling**: Add file locking, concurrency checks, and cloud storage integration.  
- **Unified Error Codes**: Standardize error codes across all modules for streamlined debugging.
