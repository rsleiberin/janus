# File: backend/utils/error_handling/utils/errors.py

from backend.utils.errors import GeneralError  # Import base error class if central system exists.

class UtilityError(GeneralError):
    """
    Base exception for all utility-related errors.
    """
    pass


class FileHandlerError(UtilityError):
    """
    Exception raised for file handler-related errors.

    Causes:
    - File not found
    - Permission denied
    - Read/write errors
    """
    pass


class SecurityError(UtilityError):
    """
    Base exception for all security-related errors.
    """
    pass


class AuthenticationError(SecurityError):
    """
    Exception raised for authentication-related issues.

    Causes:
    - Invalid credentials
    - Missing or expired tokens
    - Malformed authentication headers
    """
    pass


class AuthorizationError(SecurityError):
    """
    Exception raised for authorization-related issues.

    Causes:
    - Insufficient privileges
    - Forbidden actions
    """
    pass


class ValidationError(UtilityError):
    """
    Exception raised for input validation issues.

    Causes:
    - Invalid data format
    - Unsafe input
    - Business rule violations
    """
    pass


class HealthCheckError(UtilityError):
    """
    Exception raised for health check-related issues.

    Causes:
    - Failed system health checks
    - Dependency failures
    """
    pass
