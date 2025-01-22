# File: backend/utils/error_handling/error_handling.py

from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.db.errors import (
    DatabaseConnectionError,
    SchemaCreationError,
    SessionCommitError,
    LogNotFoundError,
)
from backend.utils.error_handling.utils.errors import GeneralError
from sqlalchemy.exc import SQLAlchemyError

# Initialize the centralized logger
logger = CentralizedLogger()

def format_error_response(status, error_code, message, details=None, meta_data=None):
    """
    Formats a standardized error response.

    Args:
        status (int): HTTP status code.
        error_code (str): Application-specific error code.
        message (str): Human-readable error message.
        details (str, optional): Detailed information about the error.
        meta_data (dict, optional): Additional context for the error.

    Returns:
        dict: A structured dictionary with error details.
    """
    response = {
        "status": status,
        "error_code": error_code,
        "message": message,
    }
    if details:
        response["details"] = details
    if meta_data:
        response["meta_data"] = meta_data
    return response

def log_error(error, module=None, user_id=None, meta_data=None):
    """
    Logs an error message using the centralized logger.

    Args:
        error (Exception or str): The error to log.
        module (str, optional): The module where the error occurred.
        user_id (int, optional): ID of the user associated with the error.
        meta_data (dict, optional): Additional context for the error.
    """
    logger.log_to_console("ERROR", str(error), module=module)
    logger.log_to_db(
        level="ERROR",
        message=str(error),
        module=module,
        user_id=user_id,
        meta_data=meta_data,
    )

def handle_database_error(error: Exception, module: str = None, meta_data: dict = None):
    """
    Handles database-related exceptions by logging them and raising a standardized exception.

    Args:
        error (Exception): The exception that was raised.
        module (str, optional): The module or context where the error occurred.
        meta_data (dict, optional): Additional metadata to provide context.

    Raises:
        DatabaseConnectionError, SchemaCreationError, SessionCommitError,
        LogNotFoundError, GeneralError: Based on the type of the original error.
    """
    # Log the error with context
    log_error(error, module=module, meta_data=meta_data)

    # Map common database-related errors to error codes and messages
    error_mapping = {
        DatabaseConnectionError: ("DB_CONNECTION_ERROR", "Failed to connect to the database."),
        SchemaCreationError: ("SCHEMA_CREATION_ERROR", "Error creating database schema."),
        SessionCommitError: ("SESSION_COMMIT_ERROR", "Failed to commit database session."),
        LogNotFoundError: ("LOG_NOT_FOUND", "Requested log entry was not found."),
        SQLAlchemyError: ("SQLALCHEMY_ERROR", "An unexpected database error occurred."),
    }

    # Determine the error code and message based on the exception type
    error_code, message = error_mapping.get(
        type(error), ("UNKNOWN_DB_ERROR", "An unknown database error occurred.")
    )

    # Raise the corresponding exception with the message
    if type(error) in error_mapping:
        if isinstance(error, DatabaseConnectionError):
            raise DatabaseConnectionError(message) from error
        elif isinstance(error, SchemaCreationError):
            raise SchemaCreationError(message) from error
        elif isinstance(error, SessionCommitError):
            raise SessionCommitError(message) from error
        elif isinstance(error, LogNotFoundError):
            raise LogNotFoundError(message) from error
        else:
            raise GeneralError(message) from error
    else:
        raise GeneralError(message) from error

def handle_general_error(error, meta_data=None):
    """
    Handles general exceptions with standardized logging and response.

    Args:
        error (Exception): The exception to handle.
        meta_data (dict, optional): Additional context for the error.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    log_error(error, module="general", meta_data=meta_data)
    response = format_error_response(
        status=500,
        error_code="GENERAL_ERROR",
        message="An unexpected error occurred.",
        details=str(error),
        meta_data=meta_data,
    )
    return response, 500

def handle_http_error(status, error_code, message, meta_data=None):
    """
    Handles predefined HTTP errors with standardized responses.

    Args:
        status (int): HTTP status code.
        error_code (str): Application-specific error code.
        message (str): Human-readable error message.
        meta_data (dict, optional): Additional context for the error.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    logger.log_to_console("WARNING", f"{status} - {message}", meta_data=meta_data)
    response = format_error_response(
        status=status,
        error_code=error_code,
        message=message,
        meta_data=meta_data,
    )
    return response, status

class ErrorContext:
    """
    Context manager for simplified error handling.

    Usage:
        with ErrorContext(module="module_name", user_id=123, meta_data={"key": "value"}):
            # Your code here
    """

    def __init__(self, module, user_id=None, meta_data=None):
        self.module = module
        self.user_id = user_id
        self.meta_data = meta_data

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value:
            log_error(
                exc_value,
                module=self.module,
                user_id=self.user_id,
                meta_data=self.meta_data,
            )
