# File: backend/utils/error_handling/exceptions.py

from sqlalchemy.exc import SQLAlchemyError


class GeneralError(Exception):
    """
    Root exception for all custom errors.
    """
    pass


class UtilityBaseError(GeneralError):
    """
    Base exception for utility-related errors.
    """
    pass


class FileHandlerError(UtilityBaseError):
    """
    Exception for file handler-related errors.
    """

    def __init__(self, message="An error occurred in the file handler.", file_name=None):
        super().__init__(message)
        self.file_name = file_name


class SecurityError(UtilityBaseError):
    """
    Base exception for security-related errors.
    """
    pass


class AuthenticationError(SecurityError):
    """
    Exception for authentication-related issues.
    (e.g., invalid credentials, missing tokens)
    """

    def __init__(self, message="Authentication failed.", user_id=None):
        super().__init__(message)
        self.user_id = user_id


class AuthorizationError(SecurityError):
    """
    Exception for authorization-related issues.
    (e.g., insufficient privileges, forbidden actions)
    """

    def __init__(self, message="Authorization failed.", action=None):
        super().__init__(message)
        self.action = action


class ValidationError(SecurityError):
    """
    Exception for input validation-related issues.
    (e.g., unsafe input, format violations)
    """

    def __init__(self, message="Validation failed.", invalid_field=None):
        super().__init__(message)
        self.invalid_field = invalid_field


class HealthCheckError(UtilityBaseError):
    """
    Exception for health check-related issues.
    """

    def __init__(self, message="Health check failed.", service_name=None):
        super().__init__(message)
        self.service_name = service_name


# Database-Related Exceptions


class DatabaseError(GeneralError):
    """Base exception for all database-related errors."""
    pass


class DatabaseConnectionError(DatabaseError):
    """Raised for database connection issues."""
    pass


class SchemaCreationError(DatabaseError):
    """Raised for database schema creation errors."""
    pass


class SessionCommitError(DatabaseError):
    """Raised for errors during database session commits."""
    pass


class LogNotFoundError(DatabaseError):
    """Raised when a log entry is not found."""
    pass


class LogError(DatabaseError):
    """Raised for log-related database errors."""
    pass


class AnalyticsError(DatabaseError):
    """Raised for analytics-related database errors."""
    pass


class ImageError(DatabaseError):
    """Raised for image-related database errors."""
    pass
