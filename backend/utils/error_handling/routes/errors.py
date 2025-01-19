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


class ImageProcessingError(Exception):
    """Raised when an error occurs during image processing."""


class ImageUploadError(Exception):
    """Raised when an error occurs during image upload."""


class ImageNotFoundError(Exception):
    """Raised when a requested image is not found."""


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
        error_mapping = {
            FileAccessError: (
                403,
                "FILE_ACCESS_DENIED",
                "Access denied to the requested file.",
            ),
            FileNotFoundErrorCustom: (
                404,
                "FILE_NOT_FOUND",
                "The requested file was not found.",
            ),
            NoAuthorizationError: (
                401,
                "MISSING_AUTHORIZATION_HEADER",
                "Missing Authorization Header",
            ),
            InvalidHeaderError: (
                401,
                "AUTHORIZATION_ERROR",
                "Token is invalid or expired.",
            ),
            AuthenticationError: (
                401,
                "AUTHENTICATION_ERROR",
                "Invalid credentials provided.",
            ),
            WeakPasswordError: (
                400,
                "WEAK_PASSWORD",
                "The provided password does not meet complexity requirements.",
            ),
            UserNotFoundError: (
                404,
                "USER_NOT_FOUND",
                "The requested user does not exist.",
            ),
            InvalidUserDataError: (
                400,
                "INVALID_USER_DATA",
                "The provided user data is invalid.",
            ),
            HealthCheckError: (
                500,
                "HEALTH_CHECK_FAILED",
                "The system health check encountered an issue.",
            ),
            ImageProcessingError: (
                500,
                "IMAGE_PROCESSING_ERROR",
                "An error occurred during image processing.",
            ),
            ImageUploadError: (
                400,
                "IMAGE_UPLOAD_ERROR",
                "An error occurred during image upload.",
            ),
            ImageNotFoundError: (
                404,
                "IMAGE_NOT_FOUND",
                "The requested image was not found.",
            ),
        }

        if error.__class__ in error_mapping:
            status, error_code, message = error_mapping[error.__class__]
            logger.log_to_console(
                "ERROR", message, details=str(error), meta_data=meta_data
            )
            return (
                format_error_response(
                    status=status,
                    error_code=error_code,
                    message=message,
                    details=str(error),
                    meta_data=meta_data,
                ),
                status,
            )

        # Handle unknown errors
        logger.log_to_console(
            "ERROR",
            "Unknown route error occurred.",
            details=str(error),
            meta_data=meta_data,
        )
        return (
            format_error_response(
                status=500,
                error_code="UNKNOWN_ROUTE_ERROR",
                message="An unknown error occurred while processing your request.",
                details=str(error),
                meta_data=meta_data,
            ),
            500,
        )

    except OperationalError as db_error:
        logger.log_to_console(
            "CRITICAL",
            "Database logging failed.",
            details=str(db_error),
            meta_data=meta_data,
        )
        return (
            format_error_response(
                status=500,
                error_code="DATABASE_LOGGING_FAILED",
                message="A database error occurred while logging the request.",
                details=str(db_error),
                meta_data=meta_data,
            ),
            500,
        )
