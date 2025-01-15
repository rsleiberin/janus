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

class HealthCheckError(Exception):
    """Raised when a health check fails due to an internal issue."""

class LogRetrievalError(Exception):
    """Raised when fetching logs encounters an error."""

class AnalyticsQueryError(Exception):
    """Raised when an analytics query fails."""

class InvalidAnalyticsRequestError(Exception):
    """Raised when an analytics request has invalid parameters."""

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
        logger.log_to_console("WARNING", "File not found.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=404,
            error_code="FILE_NOT_FOUND",
            message="The requested file was not found.",
            details=str(error),
            meta_data=meta_data,
        ), 404
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
        logger.log_to_console("ERROR", "Invalid user data.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=400,
            error_code="INVALID_USER_DATA",
            message="The provided user data is invalid.",
            details=str(error),
            meta_data=meta_data,
        ), 400
    elif isinstance(error, AnalyticsQueryError):
        logger.log_to_console("ERROR", "Analytics query failed.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=500,
            error_code="ANALYTICS_QUERY_ERROR",
            message="An error occurred while processing the analytics query.",
            details=str(error),
            meta_data=meta_data,
        ), 500
    elif isinstance(error, InvalidAnalyticsRequestError):
        logger.log_to_console("ERROR", "Invalid analytics request parameters.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=400,
            error_code="INVALID_ANALYTICS_REQUEST",
            message="The provided analytics request parameters are invalid.",
            details=str(error),
            meta_data=meta_data,
        ), 400
    elif isinstance(error, HealthCheckError):
        logger.log_to_console("ERROR", "Health check failed.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=500,
            error_code="HEALTH_CHECK_FAILED",
            message="The system health check encountered an issue.",
            details=str(error),
            meta_data=meta_data,
        ), 500
    else:
        logger.log_to_console("ERROR", "Unknown route error occurred.", details=str(error), meta_data=meta_data)
        return format_error_response(
            status=500,
            error_code="UNKNOWN_ROUTE_ERROR",
            message="An unknown error occurred while processing your request.",
            details=str(error),
            meta_data=meta_data,
        ), 500
