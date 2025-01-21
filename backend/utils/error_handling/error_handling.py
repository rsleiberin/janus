# File: backend/utils/error_handling/error_handling.py

from backend.utils.logger import CentralizedLogger

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
        tuple: A tuple containing the JSON response and the HTTP status code.
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
    return (
        format_error_response(
            status=500,
            error_code="GENERAL_ERROR",
            message="An unexpected error occurred.",
            details=str(error),
            meta_data=meta_data,
        ),
        500,
    )


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
    return (
        format_error_response(
            status=status,
            error_code=error_code,
            message=message,
            meta_data=meta_data,
        ),
        status,
    )


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


# Add new handlers for authentication and authorization errors
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
    return (
        format_error_response(
            status=401,
            error_code="AUTHENTICATION_FAILED",
            message="Authentication failed. Please check your credentials.",
            details=details,
            meta_data=meta_data,
        ),
        401,
    )


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
    return (
        format_error_response(
            status=403,
            error_code="UNAUTHORIZED_ACCESS",
            message="You are not authorized to access this resource.",
            details=details,
            meta_data=meta_data,
        ),
        403,
    )
