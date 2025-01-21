from flask_jwt_extended.exceptions import InvalidHeaderError, NoAuthorizationError
from sqlalchemy.exc import OperationalError
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import format_error_response, log_error
from backend.utils.error_handling.utils.errors import (
    AuthenticationError,
    FileHandlerError,
    HealthCheckError,
    ValidationError,
)

# Initialize centralized logger
logger = CentralizedLogger("route_errors")

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
            FileHandlerError: (
                403,
                "FILE_ACCESS_DENIED",
                "Access denied to the requested file.",
            ),
            FileNotFoundError: (
                404,
                "FILE_NOT_FOUND",
                "The requested file was not found.",
            ),
            NoAuthorizationError: (
                401,
                "MISSING_AUTHORIZATION_HEADER",
                "Missing Authorization Header.",
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
            ValidationError: (
                400,
                "INVALID_USER_DATA",
                "The provided user data is invalid.",
            ),
            HealthCheckError: (
                500,
                "HEALTH_CHECK_FAILED",
                "The system health check encountered an issue.",
            ),
        }

        if error.__class__ in error_mapping:
            status, error_code, message = error_mapping[error.__class__]
            log_error(error, module="route_errors", meta_data=meta_data)
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
        log_error(
            error,
            module="route_errors",
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
        log_error(
            db_error,
            module="route_errors",
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
