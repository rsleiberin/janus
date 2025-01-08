import uuid
from backend.utils.logger import CentralizedLogger
import os

# Initialize the centralized logger
logger = CentralizedLogger()

def format_error_response(status, error_code, message, details=None, meta_data=None):
    """
    Formats a standardized error response.

    Args:
        status (int): HTTP status code.
        error_code (str): Unique error code for tracking the error type.
        message (str): A user-friendly error message.
        details (str, optional): Detailed error information (for debugging).
        meta_data (dict, optional): Additional metadata for tracking.

    Returns:
        dict: A structured error response.
    """
    response = {
        "status": status,
        "error_code": error_code,
        "message": message,
    }
    if details is not None:
        response["details"] = details
    if meta_data:
        response["meta_data"] = meta_data
    return response


def log_error(error, module=None, user_id=None, meta_data=None):
    """
    Logs an error message using the centralized logger.

    Args:
        error (Exception): The exception to log.
        module (str): The module where the error originated.
        user_id (int, optional): ID of the user associated with the error.
        meta_data (dict, optional): Additional metadata for context.
    """
    logger.log_to_console("ERROR", str(error), module=module)
    logger.log_to_db(
        level="ERROR",
        message=str(error),
        module=module,
        user_id=user_id,
        meta_data=meta_data,
    )

def handle_general_error(error, meta_data=None):
    """
    Standardizes general error responses and logs the error.

    Args:
        error (Exception): The exception raised.
        meta_data (dict, optional): Additional context for the error.

    Returns:
        tuple: JSON response and HTTP status code.
    """
    log_error(error, module="general", meta_data=meta_data)
    return format_error_response(
        status=500,
        error_code="GENERAL_ERROR",
        message="An unexpected error occurred.",
        details=str(error),
        meta_data=meta_data,
    ), 500

def handle_http_error(status, error_code, message, meta_data=None):
    """
    Handles predefined HTTP errors with standardized responses.

    Args:
        status (int): HTTP status code.
        error_code (str): Unique error code for tracking.
        message (str): User-friendly error message.
        meta_data (dict, optional): Additional metadata.

    Returns:
        tuple: JSON response and HTTP status code.
    """
    logger.log_to_console("WARNING", f"{status} - {message}", meta_data=meta_data)
    return format_error_response(
        status=status,
        error_code=error_code,
        message=message,
        meta_data=meta_data,
    ), status

class error_context:
    """
    Context manager for simplified error handling.

    Args:
        module (str): Module where the error occurred.
        user_id (int, optional): User ID associated with the error.
        meta_data (dict, optional): Additional metadata for context.
    """
    def __init__(self, module, user_id=None, meta_data=None):
        self.module = module
        self.user_id = user_id
        self.meta_data = meta_data

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value:
            log_error(exc_value, module=self.module, user_id=self.user_id, meta_data=self.meta_data)
