from backend.utils.error_handling.error_handling import format_error_response

class DatabaseUnavailableError(Exception):
    """Raised when the database is not accessible."""

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
    else:
        return format_error_response(
            status=500,
            error_code="UNKNOWN_ROUTE_ERROR",
            message="An unknown error occurred in the route.",
            details=str(error),
            meta_data=meta_data,
        ), 500
