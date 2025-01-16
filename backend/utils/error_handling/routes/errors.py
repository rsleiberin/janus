from backend.utils.error_handling.error_handling import format_error_response
from backend.utils.logger import CentralizedLogger
from sqlalchemy.exc import OperationalError
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError

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

class WeakPasswordError(Exception):
    """Raised when a new password does not meet complexity requirements."""

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
    try:
        if isinstance(error, FileAccessError):
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
        elif isinstance(error, NoAuthorizationError):
            logger.log_to_console("ERROR", "Missing Authorization Header.", details=str(error), meta_data=meta_data)
            return format_error_response(
                status=401,
                error_code="MISSING_AUTHORIZATION_HEADER",
                message="Missing Authorization Header",
                details=str(error),
                meta_data=meta_data,
            ), 401

        elif isinstance(error, InvalidHeaderError):
            logger.log_to_console("ERROR", "Invalid token provided.", details=str(error), meta_data=meta_data)
            return format_error_response(
                status=401,
                error_code="AUTHORIZATION_ERROR",
                message="Token is invalid or expired.",
                details=str(error),
                meta_data=meta_data,
            ), 401
        elif isinstance(error, AuthenticationError):
            logger.log_to_console("ERROR", "Authentication error occurred.", details=str(error), meta_data=meta_data)
            return format_error_response(
                status=401,
                error_code="AUTHENTICATION_ERROR",
                message="Invalid credentials provided.",
                details=str(error),
                meta_data=meta_data,
            ), 401
        elif isinstance(error, WeakPasswordError):
            logger.log_to_console("ERROR", "Weak password provided.", details=str(error), meta_data=meta_data)
            return format_error_response(
                status=400,
                error_code="WEAK_PASSWORD",
                message="The provided password does not meet complexity requirements.",
                details=str(error),
                meta_data=meta_data,
            ), 400
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
    except OperationalError as db_error:
        logger.log_to_console("CRITICAL", "Database logging failed.", details=str(db_error), meta_data=meta_data)
        return format_error_response(
            status=500,
            error_code="DATABASE_LOGGING_FAILED",
            message="A database error occurred while logging the request.",
            details=str(db_error),
            meta_data=meta_data,
        ), 500
