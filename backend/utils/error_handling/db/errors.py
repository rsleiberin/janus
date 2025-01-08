from sqlalchemy.exc import SQLAlchemyError
from backend.utils.error_handling.error_handling import format_error_response, log_error

# General database error classes
class DatabaseError(Exception):
    """Base class for all database-related exceptions."""
    pass

class DatabaseConnectionError(DatabaseError):
    """Raised when there is a database connection error."""
    pass

class SchemaCreationError(DatabaseError):
    """Raised when there is an error creating the database schema."""
    pass

class SessionCommitError(DatabaseError):
    """Raised when there is an error committing a session."""
    pass

# Admin-specific error classes
class AdminNotFoundError(DatabaseError):
    """Raised when an admin record is not found."""
    pass

class AdminCreationError(DatabaseError):
    """Raised when there is an error creating an admin record."""
    pass

class AdminUpdateError(DatabaseError):
    """Raised when there is an error updating an admin record."""
    pass

# Analytics-specific error classes
class AnalyticsError(DatabaseError):
    """Base class for analytics-related exceptions."""
    pass

class AnalyticsNotFoundError(AnalyticsError):
    """Raised when an analytics entry is not found."""
    pass

class AnalyticsCreationError(AnalyticsError):
    """Raised when there is an error creating an analytics entry."""
    pass

class AnalyticsDeletionError(AnalyticsError):
    """Raised when there is an error deleting an analytics entry."""
    pass

class AnalyticsQueryError(AnalyticsError):
    """Raised when there is an error querying analytics entries."""
    pass

# Image-specific error classes
class ImageError(DatabaseError):
    """Base class for image-related exceptions."""
    pass

class ImageNotFoundError(ImageError):
    """Raised when an image record is not found."""
    pass

class ImageCreationError(ImageError):
    """Raised when there is an error creating an image record."""
    pass

class ImageUpdateError(ImageError):
    """Raised when there is an error updating an image record."""
    pass

class ImageDeletionError(ImageError):
    """Raised when there is an error deleting an image record."""
    pass

# Log-specific error classes
class LogError(DatabaseError):
    """Base class for log-related exceptions."""
    pass

class LogNotFoundError(LogError):
    """Raised when a log entry is not found."""
    pass

class LogCreationError(LogError):
    """Raised when there is an error creating a log entry."""
    pass

class LogDeletionError(LogError):
    """Raised when there is an error deleting a log entry."""
    pass

class LogQueryError(LogError):
    """Raised when there is an error querying log entries."""
    pass

class LogMetadataError(LogError):
    """Raised when there is an issue with log metadata."""
    pass

def handle_database_error(error, module=None, meta_data=None):
    """
    Handles and logs database errors.

    Args:
        error (Exception): The exception raised.
        module (str, optional): The module where the error occurred.
        meta_data (dict, optional): Additional context about the error.

    Returns:
        tuple: JSON response and HTTP status code.
    """
    log_error(error, module=module, meta_data=meta_data)

    if isinstance(error, DatabaseConnectionError):
        return format_error_response(
            status=500,
            error_code="DB_CONNECTION_ERROR",
            message="Failed to connect to the database.",
            details=str(error),
            meta_data=meta_data
        ), 500
    elif isinstance(error, SchemaCreationError):
        return format_error_response(
            status=500,
            error_code="SCHEMA_CREATION_ERROR",
            message="Failed to create the database schema.",
            details=str(error),
            meta_data=meta_data
        ), 500
    elif isinstance(error, SessionCommitError):
        return format_error_response(
            status=500,
            error_code="SESSION_COMMIT_ERROR",
            message="An error occurred while committing to the database.",
            details=str(error),
            meta_data=meta_data
        ), 500
    elif isinstance(error, AnalyticsError):
        return format_error_response(
            status=500,
            error_code="ANALYTICS_ERROR",
            message="An analytics-related error occurred.",
            details=str(error),
            meta_data=meta_data
        ), 500
    elif isinstance(error, ImageError):
        return format_error_response(
            status=500,
            error_code="IMAGE_ERROR",
            message="An image-related error occurred.",
            details=str(error),
            meta_data=meta_data
        ), 500
    elif isinstance(error, LogError):
        return format_error_response(
            status=500,
            error_code="LOG_ERROR",
            message="A log-related error occurred.",
            details=str(error),
            meta_data=meta_data
        ), 500
    elif isinstance(error, SQLAlchemyError):
        return format_error_response(
            status=500,
            error_code="SQLALCHEMY_ERROR",
            message="A general database error occurred.",
            details=str(error),
            meta_data=meta_data
        ), 500
    else:
        return format_error_response(
            status=500,
            error_code="UNKNOWN_DB_ERROR",
            message="An unknown database error occurred.",
            details=str(error),
            meta_data=meta_data
        ), 500
