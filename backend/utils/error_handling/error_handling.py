# File: backend/utils/error_handling/error_handling.py

from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.exceptions import (
    DatabaseConnectionError,
    SchemaCreationError,
    SessionCommitError,
    LogNotFoundError,
    GeneralError,
    # HealthCheckError,  # Temporarily unused
    # ImageError,        # Temporarily unused
    # FileHandlerError,  # Temporarily unused
    # SecurityError,     # Temporarily unused
    # ValidationError,   # Temporarily unused
    # AuthenticationError,  # Temporarily unused
)
from sqlalchemy.exc import SQLAlchemyError  # Temporarily unused

# Initialize the centralized logger
logger = CentralizedLogger("error_handling")


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
    Handles database-related exceptions by logging raising a standardized exception.

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

    if isinstance(error, DatabaseConnectionError):
        raise DatabaseConnectionError("Failed to connect to the database.") from error
    if isinstance(error, SchemaCreationError):
        raise SchemaCreationError("Error creating database schema.") from error
    if isinstance(error, SessionCommitError):
        raise SessionCommitError("Failed to commit database session.") from error
    if isinstance(error, LogNotFoundError):
        raise LogNotFoundError("Requested log entry was not found.") from error
    if isinstance(error, SQLAlchemyError):
        raise GeneralError(
            f"An unexpected database error occurred: {str(error)}"
        ) from error
    raise GeneralError(f"An error occurred in {module}: {str(error)}") from error


def handle_error_with_logging(
    error: Exception, module: str = None, meta_data: dict = None
):
    """
    Handles general errors by logging them and raising a standardized GeneralError.

    Args:
        error (Exception): The exception to handle.
        module (str, optional): The module or context where the error occurred.
        meta_data (dict, optional): Additional metadata for the error.

    Raises:
        GeneralError: A standardized general error.
    """
    log_error(error, module=module, meta_data=meta_data)
    raise GeneralError(f"An error occurred in {module}: {str(error)}") from error


def handle_general_error(error, meta_data=None):
    """
    Handles general exceptions with standardized logging and response.

    Args:
        error (Exception): The exception to handle.
        meta_data (dict, optional): Additional context for the error.

    Returns:
        tuple: JSON response and HTTP status code.
    """
    logger.log_to_console("ERROR", str(error), meta_data=meta_data)
    return {
        "status": 500,
        "error_code": "GENERAL_ERROR",
        "message": "An unexpected error occurred.",
        "details": str(error),
        "meta_data": meta_data,
    }, 500


def handle_authentication_error(details=None, meta_data=None):
    """
    Handles authentication errors and logs them.

    Args:
        details (str, optional): Detailed information about the error.
        meta_data (dict, optional): Additional context for the error.

    Returns:
        tuple: JSON response and HTTP status code.
    """
    log_error("Authentication failed.", module="authentication", meta_data=meta_data)
    response = format_error_response(
        status=401,
        error_code="AUTHENTICATION_FAILED",
        message="Authentication failed. Please check your credentials.",
        details=details,
        meta_data=meta_data,
    )
    return response, 401


def handle_unauthorized_error(details=None, meta_data=None):
    """
    Handles authorization errors and logs them.

    Args:
        details (str, optional): Detailed information about the error.
        meta_data (dict, optional): Additional context for the error.

    Returns:
        tuple: JSON response and HTTP status code.
    """
    log_error(
        "Unauthorized access attempt.", module="authorization", meta_data=meta_data
    )
    response = format_error_response(
        status=403,
        error_code="UNAUTHORIZED_ACCESS",
        message="You are not authorized to access this resource.",
        details=details,
        meta_data=meta_data,
    )
    return response, 403


def handle_route_error(error, meta_data=None):
    """
    Handles route-specific errors with standardized logging and response.

    Args:
        error (Exception): The exception to handle.
        meta_data (dict, optional): Additional context for the error.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    log_error(error, module="route", meta_data=meta_data)
    response = format_error_response(
        status=500,
        error_code="ROUTE_ERROR",
        message="An error occurred while processing the request.",
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


def handle_health_check_error(details=None, meta_data=None):
    """
    Handles health check-related errors and logs them.

    Args:
        details (str, optional): Detailed information about the error.
        meta_data (dict, optional): Additional context for the error.

    Returns:
        tuple: JSON response and HTTP status code.
    """
    log_error("Health check failed.", module="health_check", meta_data=meta_data)
    response = format_error_response(
        status=500,
        error_code="HEALTH_CHECK_FAILED",
        message="A health check failure occurred.",
        details=details,
        meta_data=meta_data,
    )
    return response, 500


def handle_image_error(details=None, meta_data=None):
    """
    Handles image-related errors and logs them.

    Args:
        details (str, optional): Detailed information about the error.
        meta_data (dict, optional): Additional context for the error.

    Returns:
        tuple: JSON response and HTTP status code.
    """
    log_error(
        "Image processing error occurred.",
        module="image_processing",
        meta_data=meta_data,
    )
    response = format_error_response(
        status=500,
        error_code="IMAGE_ERROR",
        message="An error occurred during image processing.",
        details=details,
        meta_data=meta_data,
    )
    return response, 500


def handle_file_handler_error(details=None, meta_data=None):
    """
    Handles file handler-related errors and logs them.

    Args:
        details (str, optional): Detailed information about the error.
        meta_data (dict, optional): Additional context for the error.

    Returns:
        tuple: JSON response and HTTP status code.
    """
    log_error(
        "File handler error occurred.", module="file_handler", meta_data=meta_data
    )
    response = format_error_response(
        status=500,
        error_code="FILE_HANDLER_ERROR",
        message="An error occurred during file handling.",
        details=details,
        meta_data=meta_data,
    )
    return response, 500


def handle_security_error(details=None, meta_data=None):
    """
    Handles security-related errors and logs them.

    Args:
        details (str, optional): Detailed information about the error.
        meta_data (dict, optional): Additional context for the error.

    Returns:
        tuple: JSON response and HTTP status code.
    """
    log_error("Security error occurred.", module="security", meta_data=meta_data)
    response = format_error_response(
        status=403,
        error_code="SECURITY_ERROR",
        message="A security error occurred.",
        details=details,
        meta_data=meta_data,
    )
    return response, 403


def handle_validation_error(details=None, meta_data=None):
    """
    Handles validation errors by logging them and returning a standardized response.

    Args:
        details (str, optional): Detailed information about the validation error.
        meta_data (dict, optional): Additional context for the error.

    Returns:
        tuple: JSON response and HTTP status code.
    """
    log_error("Validation failed.", module="validation", meta_data=meta_data)
    response = format_error_response(
        status=400,
        error_code="VALIDATION_ERROR",
        message="A validation error occurred.",
        details=details,
        meta_data=meta_data,
    )
    return response, 400


class ErrorContext:
    """
    Context manager for simplified error handling.

    Usage:
        with ErrorContext(module="module_name", user_id=123,
            meta_data={"key": "value"}):
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
