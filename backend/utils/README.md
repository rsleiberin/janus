# Utils Directory

## Overview
This directory contains utility scripts for the Janus backend. These utilities provide core functionalities such as file handling, logging configuration, error handling, and security features.

---

## Directory Structure with Implementation Stages

### **utils/**
- **file_handler.py**: Utility functions for file operations **[🚧 In Progress | Ticket #30]**
- **logger.py**: Logging configuration for the backend **[🚧 In Progress | Ticket #31]**
- **security.py**: Security utilities (e.g., input validation, sanitization) **[🚧 In Progress | Ticket #32]**
- **error_handling.py**: Centralized error handling for the backend **[🚧 In Progress | Ticket #46]**
- **README.md**: Documents the utility scripts and their functionalities **[✅ Completed]**

---

## Walkthrough of Utils

### **file_handler.py**
- **Functions**:
  - **File Uploads**: Handles uploading files and storing them in the system.
  - **File Validation**: Validates file types and sizes to ensure acceptable formats.
  - **File Replacements/Deletions**: Manages file replacements or deletions.

### **logger.py**
- **Functions**:
  - **Logging Errors, Warnings, and Debug Info**: Records various logs for backend operations. Ensures that logs are standardized across the application.
  - **Customizable Log Levels and Formatting**: Configurable log levels (e.g., INFO, DEBUG, ERROR) and log formats that allow flexibility in debugging and tracking.
  - **Compatibility with Backend Modules**: Ensures that logging integrates with other backend modules and logs relevant information for operations, errors, and debugging.

### **security.py**
- **Functions**:
  - **Input Sanitization**: Ensures data is sanitized to prevent injection attacks.
  - **Hashing and Validation of Sensitive Data**: Manages hashing of passwords or other sensitive data.
  - **Additional Security Measures**: Implements additional security mechanisms as required.

### **error_handling.py**
- **Functions**:
  - **Error Handling**: Standardizes error handling by providing structured error responses for various backend processes.
  - **Error Logging**: Captures errors with relevant context and writes them to the log for debugging and monitoring purposes.
  - **Graceful Failure**: Ensures the backend responds gracefully to failures and provides meaningful error messages to clients.
  
---

## How to Contribute
1. Add new utility functions to the appropriate file (e.g., file-related functions to `file_handler.py`).
2. Document each new function in this README.
3. Write unit tests for all new functionalities in the `tests/` directory.

---

## Best Practices
1. Keep utility scripts focused on single-domain functionality.
2. Ensure functions are reusable and well-documented.
3. Maintain secure coding practices, especially for `security.py`.
4. Ensure all errors are logged properly, and provide meaningful messages to the user in the case of failure.

---

## Relevant Tickets
- **Ticket #30**: Complete `file_handler.py` **[Phase 1]**
- **Ticket #31**: Finalize `logger.py` **[Phase 1]**
- **Ticket #32**: Implement `security.py` **[Phase 2]**
- **Ticket #33**: Add Test Cases for utils Scripts **[Phase 2]**
- **Ticket #34**: Expand utils Functionality **[Future]**
- **Ticket #46**: Implement `error_handling.py` **[Phase 2]**
