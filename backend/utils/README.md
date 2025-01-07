# Utils Directory

## Overview
This directory contains utility scripts for the Janus backend. These utilities provide core functionalities such as file handling, logging configuration, error handling, and security features. The directory is designed for modularity and scalability, ensuring that utility functions are reusable and easy to integrate across the backend.

---

## Directory Structure

### **utils/**
- **file_handler.py**: Utility functions for file operations **[🚧 In Progress | Ticket #30]**
- **logger.py**: Centralized logging configuration for the backend **[✅ Completed | Ticket #9]**
- **security.py**: Security utilities (e.g., input validation, sanitization) **[🚧 In Progress | Ticket #32]**
- **error_handling/**:
  - **api/errors.py**: Error handling for API-related operations **[🚧 In Progress | Ticket #58]**
  - **db/errors.py**: Error handling for database-related operations **[🚧 In Progress | Ticket #58]**
  - **extensions/errors.py**: Error handling for extensions **[🚧 In Progress | Ticket #58]**
  - **routes/errors.py**: Error handling for routes **[🚧 In Progress | Ticket #58]**
  - **tests/errors.py**: Error handling for test cases **[🚧 In Progress | Ticket #58]**
  - **utils/errors.py**: General error handling for utilities **[🚧 In Progress | Ticket #58]**
- **README.md**: Documents the utility scripts and their functionalities **[🚧 In Progress | Ticket #61]**

---

## Logger Module (`logger.py`)

### Overview
The `logger.py` module provides centralized logging functionality for the backend, supporting both console and database logging. It ensures all logs are consistent, structured, and enriched with contextual metadata.

### Key Features
- **Console Logging**: Logs messages to the console with optional metadata.
- **Database Logging**: Stores logs in the database for searchability and auditing.
- **Structured Format**: Formats logs in a machine-readable JSON structure.
- **Extensibility**: Prepared for integration with real-time monitoring tools.

---

## Completed Work: Logger Refactor

### **Enhancements Made**
1. **Centralized Logging**:
   - Unified logging configuration for console and database outputs.
   - Replaced legacy logging with `CentralizedLogger`.

2. **Granular Metadata Support**:
   - Implemented metadata fields such as module, user ID, and custom key-value pairs for detailed logging.

3. **Standardized Formats**:
   - Logs follow a consistent format for readability and machine parsing.

4. **Database Integration**:
   - Added support for logging critical events to the database for auditing purposes.
   - Enhanced the `Log` model to include fields for timestamp, log level, module, and metadata.

5. **Testing**:
   - Unit tests for `logger.py` have been written and validated.
   - All tests pass, ensuring robust logging functionality.

---

## Integration Plan

### Goals
1. Replace obsolete error-handling mechanisms with `CentralizedLogger`.
2. Integrate `logger.py` into all backend modules, ensuring consistent and context-rich logging.
3. Log critical actions and errors across the system, supporting both operational and audit needs.

### Steps
1. **Audit Logging Points**:
   - Identify all locations in the backend where logging is required.
   - Replace existing logs with `CentralizedLogger` where applicable.

2. **Implement Logging**:
   - Use `log_to_console` for real-time feedback and debugging.
   - Use `log_to_db` for long-term storage and auditing of critical events.

3. **Validation**:
   - Write integration tests to ensure logging works as expected across modules.
   - Mock `log_to_db` during tests to avoid unnecessary database writes.

---

## Relevant Tickets
- **Ticket #9**: Refactor and Enhance `logger.py` **[Phase 1 | Completed]**
- **Ticket #30**: Complete `file_handler.py` **[Phase 1]**
- **Ticket #32**: Implement `security.py` **[Phase 1]**
- **Ticket #58**: Centralized Error Handling for `utils` Directory **[Phase 1]**
- **Ticket #59**: Integrate Error Handling Modules Across Backend **[Phase 1]**
- **Ticket #60**: Write Test Cases for `utils` Submodules **[Phase 1]**
- **Ticket #61**: Document `utils` Directory Structure and Usage **[Phase 1]**
