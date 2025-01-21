# File: backend/utils/error_handling/utils/errors.py

class GeneralError(Exception):
    """
    Root exception for all custom errors.
    """
    pass


class UtilityBaseError(GeneralError):
    """
    Base exception for utility-related errors.
    """
    pass


class FileHandlerError(UtilityBaseError):
    """
    Exception for file handler-related errors.
    """
    def __init__(self, message="An error occurred in the file handler.", file_name=None):
        super().__init__(message)
        self.file_name = file_name


class SecurityError(UtilityBaseError):
    """
    Base exception for security-related errors.
    """
    pass


class AuthenticationError(SecurityError):
    """
    Exception for authentication-related issues.
    (e.g., invalid credentials, missing tokens)
    """
    def __init__(self, message="Authentication failed.", user_id=None):
        super().__init__(message)
        self.user_id = user_id


class AuthorizationError(SecurityError):
    """
    Exception for authorization-related issues.
    (e.g., insufficient privileges, forbidden actions)
    """
    def __init__(self, message="Authorization failed.", action=None):
        super().__init__(message)
        self.action = action


class ValidationError(SecurityError):
    """
    Exception for input validation-related issues.
    (e.g., unsafe input, format violations)
    """
    def __init__(self, message="Validation failed.", invalid_field=None):
        super().__init__(message)
        self.invalid_field = invalid_field


class HealthCheckError(UtilityBaseError):
    """
    Exception for health check-related issues.
    """
    def __init__(self, message="Health check failed.", service_name=None):
        super().__init__(message)
        self.service_name = service_name


# Example of how to include metadata for debugging/logging
def handle_error_with_logging(error: Exception, **kwargs):
    """
    Handle errors by logging metadata for easier debugging.

    Args:
        error (Exception): The exception instance to handle.
        **kwargs: Additional metadata related to the error context.

    Returns:
        dict: A structured dictionary with error details for further handling.
    """
    error_details = {
        "error_type": type(error).__name__,
        "message": str(error),
        "metadata": kwargs
    }
    # Example logging statement (replace with actual logger in use)
    print(f"Error logged: {error_details}")
    return error_details
