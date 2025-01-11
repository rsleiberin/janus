from backend.utils.error_handling.error_handling import format_error_response
from backend.utils.logger import CentralizedLogger

# Initialize centralized logger for error handling
logger = CentralizedLogger("route_errors")

# Custom Exceptions
class DatabaseUnavailableError(Exception):
    """Raised when the database is not accessible."""


class FileAccessError(Exception):
    """Raised when there is an issue accessing a file."""


class FileNotFoundErrorCustom(Exception):
    """Raised when a requested file is not found."""


class UnauthorizedError(Exception):
    """Raised when a user is unauthorized to access a resource."""


class AuthenticationError(Exception):
    """Raised when authentication fails."""


class UserNotFoundError(Exception):
    """Raised when the requested user is not found."""


class InvalidUserDataError(Exception):
    """Raised when provided user data is invalid or incomplete."""


class UnauthorizedAccessError(Exception):
    """Raised when a user tries to perform an unauthorized action."""


# Error Handlers
def handle_route_error(error, meta_data=None):
    """
    Handles route-specific errors.

    Args:
        error (Exception): The raised exception.
        meta_data (dict, optional): Additional context about the error.

    Returns:
        tuple: A JSON response and HTTP status code.
    """
    if isinstance(error, DatabaseUnavailableError):
        logger.log_to_console("ERROR", "Database is unavailable.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=500,
            error_code="DATABASE_UNAVAILABLE",
            message="The database is not accessible at the moment.",
            details=str(error),
            meta_data=meta_data,
        ), 500
    elif isinstance(error, FileAccessError):
        logger.log_to_console("ERROR", "File access denied.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=403,
            error_code="FILE_ACCESS_DENIED",
            message="Access denied to the requested file.",
            details=str(error),
            meta_data=meta_data,
        ), 403
    elif isinstance(error, FileNotFoundErrorCustom):
        logger.log_to_console("WARNING", "Requested file not found.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=404,
            error_code="FILE_NOT_FOUND",
            message="The requested file was not found.",
            details=str(error),
            meta_data=meta_data,
        ), 404
    elif isinstance(error, UnauthorizedError):
        logger.log_to_console("ERROR", "Unauthorized access attempt.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=401,
            error_code="UNAUTHORIZED",
            message="You are not authorized to access this resource.",
            details=str(error),
            meta_data=meta_data,
        ), 401
    elif isinstance(error, AuthenticationError):
        logger.log_to_console("ERROR", "Authentication failed.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=401,
            error_code="AUTHENTICATION_FAILED",
            message="Authentication failed. Please check your credentials.",
            details=str(error),
            meta_data=meta_data,
        ), 401
    elif isinstance(error, UserNotFoundError):
        logger.log_to_console("WARNING", "User not found.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=404,
            error_code="USER_NOT_FOUND",
            message="The requested user does not exist.",
            details=str(error),
            meta_data=meta_data,
        ), 404
    elif isinstance(error, InvalidUserDataError):
        logger.log_to_console("ERROR", "Invalid user data provided.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=400,
            error_code="INVALID_USER_DATA",
            message="The provided user data is invalid or incomplete.",
            details=str(error),
            meta_data=meta_data,
        ), 400
    elif isinstance(error, UnauthorizedAccessError):
        logger.log_to_console("ERROR", "Unauthorized access attempt.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=403,
            error_code="UNAUTHORIZED_ACCESS",
            message="You do not have permission to perform this action.",
            details=str(error),
            meta_data=meta_data,
        ), 403
    else:
        logger.log_to_console("ERROR", "Unknown route error occurred.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=500,
            error_code="UNKNOWN_ROUTE_ERROR",
            message="An unknown error occurred while processing your request.",
            details=str(error),
            meta_data=meta_data,
        ), 500
