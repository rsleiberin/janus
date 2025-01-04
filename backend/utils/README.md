# Utils Directory

## Overview
This directory contains utility scripts for the Janus backend. These utilities provide core functionalities such as file handling, logging configuration, error handling, and security features. The directory is designed for modularity and scalability, ensuring that utility functions are reusable and easy to integrate across the backend.

The current focus is on refactoring and enhancing the `logger.py` module to adhere to best practices and support the backend's agentic framework.

---

## Directory Structure with Implementation Stages

### **utils/**
- **file_handler.py**: Utility functions for file operations **[🚧 In Progress | Ticket #30]**
- **logger.py**: Logging configuration for the backend **[🚧 In Progress | Ticket #9]**
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

## Current Work: Logger Refactor

### **Why Refactor the Logger?**
The existing `logger.py` implementation is functional but does not adhere to best practices for scalability or centralized logging. The backend relies on logging as a primary source of truth for both debugging and real-time system monitoring. By enhancing the logger:
1. We ensure all logs are consistent, structured, and searchable.
2. We provide a unified interface for logging across the application.
3. We enable future expansion, such as integrating remote logging services or monitoring dashboards.

### **Goals of the Refactor**
1. Centralize logging to ensure consistency across all backend modules.
2. Store logs in the database to facilitate granular auditing and searchability.
3. Implement log levels and metadata for context-rich logging (e.g., module, user ID, and timestamp).
4. Unify logs to support both agents and human users with a machine-parsable yet human-readable format.
5. Ensure compatibility with real-time log monitoring in future development phases.

### **Best Practices Followed**
1. **Centralized Logging**: Use a single logger configuration shared across the application.
2. **Granular Metadata**: Include fields such as user ID, module name, and custom metadata for detailed insights.
3. **Database Integration**: Write logs to the database for searchability and auditing.
4. **Format Consistency**: Ensure logs are formatted in a human-readable yet machine-parsable structure.
5. **Security**: Protect sensitive log data by adhering to secure coding practices, such as hashing or access control.
6. **Extensibility**: Keep the implementation flexible to support future integration with external logging services.

### **Additional Considerations**
1. **Log Storage and Retention**:
   - Implement policies for log retention and archiving to manage database size.
   - Prepare for migration to external storage services when scaling demands increase.
2. **Error Handling Integration**:
   - Ensure error handling modules write all relevant error logs via `logger.py`.
   - Centralize error logging to maintain consistency and traceability.
3. **Real-Time Monitoring**:
   - Design the logger to integrate with real-time monitoring tools in the future.
4. **Agent Integration**:
   - Ensure agent-specific logs are tagged with appropriate user IDs and metadata for differentiation.

---

## Steps in Progress
1. **Enhancing Logger Functionality**:
   - Add methods for database integration.
   - Implement granular metadata support.
   - Standardize log formats across the backend.

2. **Updating Dependencies**:
   - Audit files currently using Python's built-in logging module.
   - Replace standard `logging` imports with the centralized `logger.py` module.

3. **Database Model Updates**:
   - Update the `Log` model to include fields for user ID, module name, timestamp, log level, and message content.

4. **Testing**:
   - Write unit tests for all new functionality in `logger.py`.
   - Write integration tests to verify logs are correctly stored in the database.
   - Test edge cases, concurrency, and performance benchmarks for logging.

5. **Documentation**:
   - Update this README with finalized usage instructions for the logger.
   - Document the centralized logging design in the main project README.

6. **Integration**:
   - Ensure all modules in `db/`, `routes/`, `utils/`, and `extensions/` are integrated with `logger.py`.

---

## Relevant Tickets
- **Ticket #9**: Refactor and Enhance `logger.py` **[Phase 1]**
- **Ticket #30**: Complete `file_handler.py` **[Phase 1]**
- **Ticket #32**: Implement `security.py` **[Phase 1]**
- **Ticket #58**: Centralized Error Handling for `utils` Directory **[Phase 1]**
- **Ticket #59**: Integrate Error Handling Modules Across Backend **[Phase 1]**
- **Ticket #60**: Write Test Cases for `utils` Submodules **[Phase 1]**
- **Ticket #61**: Document `utils` Directory Structure and Usage **[Phase 1]**
