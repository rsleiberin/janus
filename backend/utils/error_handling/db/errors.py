from sqlalchemy.exc import SQLAlchemyError
from backend.utils.error_handling.error_handling import format_error_response, log_error

# Base Database Error
class DatabaseError(Exception):
    """Base class for all database-related exceptions."""
    pass

# Centralized Error Types
class DatabaseConnectionError(DatabaseError):
    """Raised when there is a database connection error."""
    pass

class SchemaCreationError(DatabaseError):
    """Raised when there is an error creating the database schema."""
    pass

class SessionCommitError(DatabaseError):
    """Raised when there is an error committing a session."""
    pass

class UserError(DatabaseError):
    """Base class for user-related exceptions."""
    pass

class SecurityError(DatabaseError):
    """Base class for security-related exceptions."""
    pass

class LogError(DatabaseError):
    """Base class for log-related exceptions."""
    pass

class AnalyticsError(DatabaseError):
    """Base class for analytics-related exceptions."""
    pass

class MultiModelError(DatabaseError):
    """Base class for multi-model-related exceptions."""
    pass

# Error Handling Function
def handle_database_error(error: Exception, module: str = None, meta_data: dict = None):
    """
    Handles database-related exceptions by logging them and returning a standardized response.

    Args:
        error (Exception): The raised exception.
        module (str, optional): The module where the error occurred.
        meta_data (dict, optional): Additional metadata for context.

    Returns:
        tuple: JSON response and HTTP status code.
    """
    log_error(error, module=module, meta_data=meta_data)

    # Map common SQLAlchemy and database-specific errors
    error_mapping = {
        DatabaseConnectionError: ("DB_CONNECTION_ERROR", "Failed to connect to the database."),
        SchemaCreationError: ("SCHEMA_CREATION_ERROR", "Failed to create the database schema."),
        SessionCommitError: ("SESSION_COMMIT_ERROR", "Failed to commit changes to the database."),
        SQLAlchemyError: ("SQLALCHEMY_ERROR", "A general database error occurred."),
    }

    # Default error response
    error_code, message = error_mapping.get(type(error), ("UNKNOWN_DB_ERROR", "An unknown database error occurred."))
    
    response = format_error_response(
        status=500,
        error_code=error_code,
        message=message,
        details=str(error),
        meta_data=meta_data,
    )
    return response, 500
