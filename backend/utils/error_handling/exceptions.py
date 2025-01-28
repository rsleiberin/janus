"""
Custom exception hierarchy for the backend.

All exceptions ultimately derive from GeneralError.
"""


class GeneralError(Exception):
    """Root exception for all custom errors."""


class UtilityBaseError(GeneralError):
    """
    Base exception for utility-related errors (file handling, security checks, etc.).
    """


class FileHandlerError(UtilityBaseError):
    """
    Exception for file handler-related errors.

    Attributes:
        file_name (str, optional): The name of the file involved in the error.
    """

    def __init__(
        self, message="An error occurred in the file handler.", file_name=None
    ):
        super().__init__(message)
        self.file_name = file_name


class SecurityError(UtilityBaseError):
    """
    Base exception for security-related errors (authentication, authorization, etc.).
    """


class AuthenticationError(SecurityError):
    """
    Exception for authentication-related issues (e.g., invalid credentials or tokens).

    Attributes:
        user_id (str, optional): ID of the user associated with this auth error.
    """

    def __init__(self, message="Authentication failed.", user_id=None):
        super().__init__(message)
        self.user_id = user_id


class AuthorizationError(SecurityError):
    """
    Exception for auth-related issues (e.g., forbidden actions, insufficient role).

    Attributes:
        action (str, optional): Action attempted that triggered this auth failure.
    """

    def __init__(self, message="Authorization failed.", action=None):
        super().__init__(message)
        self.action = action


class ValidationError(SecurityError):
    """
    Exception for input validation-related issues (e.g., unsafe or invalid input).

    Attributes:
        invalid_field (str, optional): Name of the field that failed validation.
    """

    def __init__(self, message="Validation failed.", invalid_field=None):
        super().__init__(message)
        self.invalid_field = invalid_field


class HealthCheckError(UtilityBaseError):
    """
    Exception for health check-related issues.

    Attributes:
        service_name (str, optional): Name of the service or subsystem that failed.
    """

    def __init__(self, message="Health check failed.", service_name=None):
        super().__init__(message)
        self.service_name = service_name


# -----------------------------------------------------------------------
# Database-related exceptions
# -----------------------------------------------------------------------


class DatabaseError(GeneralError):
    """Base exception for all database-related errors."""


class DatabaseConnectionError(DatabaseError):
    """Raised for DB connection issues (cannot establish or maintain a DB connection)"""


class SchemaCreationError(DatabaseError):
    """Raised for DB schema creation errors (migrations or table creation failures)."""


class SessionCommitError(DatabaseError):
    """Raised for errors during DB session commits (e.g., constraint violations)."""


class LogNotFoundError(DatabaseError):
    """Raised when a log entry is not found in the database."""


class LogError(DatabaseError):
    """Raised for log-related DB errors (e.g., insertion or retrieval failures)."""


class AnalyticsError(DatabaseError):
    """Raised for analytics-related database errors (e.g., query or data processing)."""


class ImageError(DatabaseError):
    """Raised for image-related database errors (e.g., missing records for images)."""
