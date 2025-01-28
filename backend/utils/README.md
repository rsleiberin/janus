# Utilities (utils)

This directory provides **modular utility functions** and **supporting classes** for the Janus backend. Each file focuses on a distinct responsibility, enabling clear separation of concerns and reusable functionality.

---

## Table of Contents

1. [Overview](#overview)  
2. [Modules](#modules)  
   - [file_handler.py](#file_handlerpy)  
   - [logger.py](#loggerpy)  
   - [security.py](#securitypy)  
   - [error_handling/](#error_handling)  
   - [code_quality.py](#code_qualitypy)  
3. [Development Best Practices](#development-best-practices)  
4. [Future Enhancements](#future-enhancements)  
5. [Audit Observations](#audit-observations)

---

## Overview

The `utils` directory contains **shared utilities** utilized across the entire backend. By centralizing common logic—such as file operations, logging, security checks, and error handling—the project maintains a **clean and maintainable** architecture.

---

## Modules

### file_handler.py
- **Purpose**: Read, write, and delete files in a secure and consistent manner.
- **Key Features**:
  1. **Safe Path Construction**: Builds file paths per user to avoid collisions or path traversal vulnerabilities.
  2. **Filename Validation**: Rejects suspicious filenames via regex checks.
  3. **Error Handling**: Wraps file operations in custom exceptions for clarity and logs details through a centralized logger.

### logger.py
- **Purpose**: Provides a **centralized** logging mechanism.
- **Key Features**:
  1. **Console & DB Logging**: Logs critical data both to the console (via `StreamHandler`) and the application database (`Log` model).
  2. **Structured Messages**: Appends extra context/metadata in JSON format for easier analysis.
  3. **Dynamic Log Levels**: Reads from environment variables (or constructor args) to quickly switch log verbosity.

### security.py
- **Purpose**: Manages authentication, authorization, and basic input validation/sanitization.
- **Key Features**:
  1. **Authentication**: Simple credential checks (placeholder logic for demonstration).
  2. **Authorization**: Role-based checks ensuring that only appropriate users can access restricted resources.
  3. **Input Validation & Sanitization**: Protects the system from malicious input (e.g., JavaScript tags, invalid characters).

### error_handling/
- **Purpose**: Centralizes all exception classes and error-handling routines to maintain consistent behavior when issues arise.
- **Key Files**:
  1. **error_handling.py**: Defines functions to capture, log, and format errors (HTTP or otherwise), plus an `ErrorContext` for automatic logging within `with` blocks.
  2. **exceptions.py**: Declares custom exceptions like `FileHandlerError`, `SecurityError`, `DatabaseError`, etc., for precise error reporting.

### code_quality.py
- **Purpose**: Automates linting and formatting checks using **Flake8** and **Black**.
- **Key Features**:
  1. **`run_flake8()`**: Scans the codebase for style or syntax infractions and exits with an error code if found.
  2. **`run_black()`**: Checks if the code is Black-formatted and fails if reformatting is needed.
  3. **Subprocess Management**: Encapsulates calls to external tools so the rest of the codebase can remain tool-agnostic.

---

## Development Best Practices

1. **Single Responsibility**  
   Each module focuses on a tightly scoped responsibility, preventing feature creep and keeping dependencies minimal.

2. **Strong Typing & Clear Docstrings**  
   Although not all functions use type hints, consider adding them where clarity benefits. Keep docstrings in sync with code changes.

3. **Centralized Error Handling**  
   Whenever possible, **log and raise** exceptions in a consistent, centralized manner. The `ErrorContext` and specialized exceptions in `exceptions.py` provide structured error management.

4. **Security in Mind**  
   - Validate inputs at boundaries.  
   - Use caution with file paths and external commands.  
   - Expand the placeholder auth logic with a real identity management system when going to production.

5. **Continuous Code Quality**  
   - Keep lines under 88 characters for PEP 8 compliance.  
   - Regularly run `run_flake8` and `run_black` (or integrate them into your CI) to maintain style consistency.  
   - Address warnings in a timely manner—do not accumulate “technical debt” in lint checks.

6. **Reuse & Modularize**  
   - If a function is helpful across modules, consider placing it here in `utils` to avoid duplication.  
   - If it becomes too large or specialized, break it out into its own module.

---

## Future Enhancements

1. **Advanced Security**  
   - Replace placeholder authentication with robust identity management (e.g., OAuth2, JWT validations against real user data).  
   - Add deeper input sanitization or library-based HTML escaping.

2. **Logging to Multiple Backends**  
   - Extend `logger.py` to support streaming logs to external services (e.g., ELK stack, Sentry).

3. **More Granular Error Classes**  
   - Reintroduce or expand commented-out exceptions (e.g., `HealthCheckError`, `ImageError`) as the application’s features evolve.

4. **CI/CD Integration**  
   - Automate `flake8` and `black` checks with each push or pull request for consistent code quality.

5. **Performance Profiling**  
   - Insert instrumentation or tracing if the utility code handles large files or high traffic.

---

## Audit Observations

- **Overall**: Existing docstrings are consistent and follow a clear, readable style. Each utility file has clear docstrings at the function/class level, which helps maintain code quality and clarity.
- **Module-Level Docstrings**: Some files (e.g., `logger.py`) could optionally include a short top-level module docstring describing the module’s purpose. This isn’t strictly required but can enhance consistency.
- **Type Hints**: The current code rarely uses Python type hints (e.g., `def function(arg: str) -> bool:`). While docstrings are sufficient for describing parameters, adding type hints can further clarify usage.
- **Inactive Exceptions**: The `error_handling.py` file has several commented-out exception imports. If they’re truly no longer needed, removing them could simplify the code. Alternatively, if they’re planned for future use, consider moving them to a “future tasks” section or clarifying their eventual purpose in docstrings.
- **No Major Refactors Needed**: All files already pass linting and remain well-structured. No significant structural changes or rewrites appear necessary at this time.
