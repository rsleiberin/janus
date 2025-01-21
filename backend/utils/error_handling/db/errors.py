from sqlalchemy.exc import SQLAlchemyError
from backend.utils.error_handling.error_handling import format_error_response, log_error

# Base Database Error
class DatabaseError(Exception):
    """Base exception for all database-related errors."""
    pass


# Specific Database Errors
class DatabaseConnectionError(DatabaseError):
    """Raised for database connection issues."""
    pass


class SchemaCreationError(DatabaseError):
    """Raised for database schema creation errors."""
    pass


class SessionCommitError(DatabaseError):
    """Raised for errors during database session commits."""
    pass


class UserError(DatabaseError):
    """Raised for user-related database errors."""
    pass


class SecurityError(DatabaseError):
    """Raised for security-related database errors."""
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


# Centralized Error Handler
def handle_database_error(error: Exception, module: str = None, meta_data: dict = None):
    """
    Handles database-related exceptions by logging them and returning a standardized response.

    Args:
        error (Exception): The exception that was raised.
        module (str, optional): The module or context where the error occurred.
        meta_data (dict, optional): Additional metadata to provide context.

    Returns:
        tuple: A formatted error response (JSON) and HTTP status code.
    """
    # Log the error with context
    log_error(error, module=module, meta_data=meta_data)

    # Map common database-related errors to responses
    error_mapping = {
        DatabaseConnectionError: ("DB_CONNECTION_ERROR", "Failed to connect to the database."),
        SchemaCreationError: ("SCHEMA_CREATION_ERROR", "Error creating database schema."),
        SessionCommitError: ("SESSION_COMMIT_ERROR", "Failed to commit database session."),
        LogNotFoundError: ("LOG_NOT_FOUND", "Requested log entry was not found."),
        SQLAlchemyError: ("SQLALCHEMY_ERROR", "An unexpected database error occurred."),
    }

    # Fallback for unknown error types
    error_code, message = error_mapping.get(
        type(error), ("UNKNOWN_DB_ERROR", "An unknown database error occurred.")
    )

    # Build and return the standardized error response
    response = format_error_response(
        status=500,
        error_code=error_code,
        message=message,
        details=str(error),
        meta_data=meta_data,
    )
    return response, 500
