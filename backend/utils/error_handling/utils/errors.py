# errors.py

from backend.utils.error_handling.error_handling import log_error

class UtilityBaseError(Exception):
    """
    Base exception for utility-related errors.
    """
    pass

class FileHandlerError(UtilityBaseError):
    """
    Exception for file handler-related errors.
    """
    pass

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
    pass

class AuthorizationError(SecurityError):
    """
    Exception for authorization-related issues.
    (e.g., insufficient privileges, forbidden actions)
    """
    pass

class ValidationError(SecurityError):
    """
    Exception for input validation-related issues.
    (e.g., unsafe input, format violations)
    """
    pass

def handle_utility_error(error, module=None, user_id=None, meta_data=None):
    """
    Logs and raises or returns a standardized error for utility operations.
    
    Args:
        error (Exception): The utility-related exception.
        module (str, optional): The module where the error originated.
        user_id (int, optional): ID of the user encountering the error.
        meta_data (dict, optional): Additional context or metadata.
    
    Raises:
        Exception: Re-raises the original error after logging.
    """
    log_error(error, module=module, user_id=user_id, meta_data=meta_data)
    raise error
