# File: backend/utils/__init__.py

from .logger import CentralizedLogger
from .file_handler import (
    construct_file_path,
    is_valid_filename,
    read_file,
    write_file,
    delete_file,
)
from .security import (
    check_authentication,
    check_authorization,
    validate_input,
    sanitize_input,
)
from .error_handling import (
    handle_database_error,
    handle_error_with_logging,
    handle_general_error,
    handle_authentication_error,
    handle_unauthorized_error,
    handle_route_error,
    handle_http_error,
    handle_health_check_error,
    handle_image_error,
    handle_file_handler_error,
    handle_security_error,
    handle_validation_error,
    ErrorContext,
)

__all__ = [
    "CentralizedLogger",
    "construct_file_path",
    "is_valid_filename",
    "read_file",
    "write_file",
    "delete_file",
    "check_authentication",
    "check_authorization",
    "validate_input",
    "sanitize_input",
    "handle_database_error",
    "handle_error_with_logging",
    "handle_general_error",
    "handle_authentication_error",
    "handle_unauthorized_error",
    "handle_route_error",
    "handle_http_error",
    "handle_health_check_error",
    "handle_image_error",
    "handle_file_handler_error",
    "handle_security_error",
    "handle_validation_error",
    "ErrorContext",
]
