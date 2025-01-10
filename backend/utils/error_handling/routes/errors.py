from backend.utils.error_handling.error_handling import format_error_response

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
    """Raised when a requested user is not found."""

class InvalidUserDataError(Exception):
    """Raised when provided user data is invalid or incomplete."""

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
        return format_error_response(
            status=500,
            error_code="DATABASE_UNAVAILABLE",
            message="The database is not accessible at the moment.",
            details=str(error),
            meta_data=meta_data,
        ), 500
    elif isinstance(error, FileAccessError):
        return format_error_response(
            status=403,
            error_code="FILE_ACCESS_DENIED",
            message="Access denied to the requested file.",
            details=str(error),
            meta_data=meta_data,
        ), 403
    elif isinstance(error, FileNotFoundErrorCustom):
        return format_error_response(
            status=404,
            error_code="FILE_NOT_FOUND",
            message="The requested file was not found.",
            details=str(error),
            meta_data=meta_data,
        ), 404
    elif isinstance(error, UnauthorizedError):
        return format_error_response(
            status=401,
            error_code="UNAUTHORIZED",
            message="You are not authorized to access this resource.",
            details=str(error),
            meta_data=meta_data,
        ), 401
    elif isinstance(error, AuthenticationError):
        return format_error_response(
            status=401,
            error_code="AUTHENTICATION_FAILED",
            message="Authentication failed. Please check your credentials.",
            details=str(error),
            meta_data=meta_data,
        ), 401
    elif isinstance(error, UserNotFoundError):
        return format_error_response(
            status=404,
            error_code="USER_NOT_FOUND",
            message="The requested user was not found.",
            details=str(error),
            meta_data=meta_data,
        ), 404
    elif isinstance(error, InvalidUserDataError):
        return format_error_response(
            status=400,
            error_code="INVALID_USER_DATA",
            message="The provided user data is invalid or incomplete.",
            details=str(error),
            meta_data=meta_data,
        ), 400
    else:
        return format_error_response(
            status=500,
            error_code="UNKNOWN_ROUTE_ERROR",
            message="An unknown error occurred in the route.",
            details=str(error),
            meta_data=meta_data,
        ), 500
