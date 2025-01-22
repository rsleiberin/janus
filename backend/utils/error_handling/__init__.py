# File: backend/utils/error_handling/__init__.py

from .error_handling import (
    handle_database_error,
    handle_error_with_logging,
    handle_general_error,
    handle_authentication_error,
    handle_unauthorized_error,
    handle_route_error,
    handle_http_error,
)
from .exceptions import (
    DatabaseConnectionError,
    SchemaCreationError,
    SessionCommitError,
    LogNotFoundError,
    GeneralError,
    HealthCheckError,
    ImageError,            # Ensure all custom exceptions are included
    FileHandlerError,      # Add any other custom exceptions as needed
    SecurityError,         # Example additional exception
)

__all__ = [
    "handle_database_error",
    "handle_error_with_logging",
    "handle_general_error",
    "handle_authentication_error",
    "handle_unauthorized_error",
    "handle_route_error",
    "handle_http_error",
    "DatabaseConnectionError",
    "SchemaCreationError",
    "SessionCommitError",
    "LogNotFoundError",
    "GeneralError",
    "HealthCheckError",
    "ImageError",
    "FileHandlerError",
    "SecurityError",
]
