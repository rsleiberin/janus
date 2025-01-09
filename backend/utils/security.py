# security.py

import re
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import error_context, log_error
from backend.utils.error_handling.utils.errors import (
    AuthenticationError,
    AuthorizationError,
    ValidationError
)

logger = CentralizedLogger(name="security_logger")


def check_authentication(credentials):
    """
    Verifies user credentials. Raises AuthenticationError if invalid.

    Args:
        credentials (dict): A dictionary containing authentication info, 
                            e.g., {"username": "...", "password": "..."}

    Returns:
        bool: True if authentication succeeds.

    Raises:
        AuthenticationError: If credentials are invalid.
    """
    with error_context(module="security", meta_data={"operation": "authentication"}):
        # Example check (replace with real authentication logic)
        username = credentials.get("username")
        password = credentials.get("password")

        if not username or not password:
            raise AuthenticationError("Missing credentials.")

        # Dummy logic for demonstration:
        if username != "admin" or password != "password":
            raise AuthenticationError("Invalid username or password.")

        logger.log_to_console("INFO", "User authenticated successfully.")
        return True


def check_authorization(user_role, required_role):
    """
    Ensures the user's role meets or exceeds the required_role.
    Raises AuthorizationError if insufficient.

    Args:
        user_role (str): The role of the current user (e.g., 'user', 'admin').
        required_role (str): The role required to perform the action (e.g., 'admin').

    Returns:
        bool: True if authorization succeeds.

    Raises:
        AuthorizationError: If user_role is insufficient to meet required_role.
    """
    with error_context(module="security", meta_data={"operation": "authorization"}):
        # Example logic: only 'admin' can access certain resources
        if user_role != required_role:
            raise AuthorizationError(f"User role '{user_role}' does not meet requirement '{required_role}'.")

        logger.log_to_console("INFO", "User authorized successfully.")
        return True


def validate_input(input_data, pattern=r"^[a-zA-Z0-9_]+$"):
    """
    Validates input data against a given regex pattern.
    Raises ValidationError if the input is invalid.

    Args:
        input_data (str): The user-provided data to validate.
        pattern (str): The regex pattern to validate against.

    Returns:
        bool: True if validation succeeds.

    Raises:
        ValidationError: If input fails the specified pattern.
    """
    with error_context(module="security", meta_data={"operation": "validate_input"}):
        if not re.match(pattern, input_data or ""):
            raise ValidationError(f"Input '{input_data}' does not match required pattern.")

        logger.log_to_console("INFO", f"Input validation succeeded for: {input_data}")
        return True


def sanitize_input(input_string):
    """
    Demonstrates a simple sanitization process by stripping HTML tags.

    Args:
        input_string (str): The raw input to sanitize.

    Returns:
        str: The sanitized string.
    """
    with error_context(module="security", meta_data={"operation": "sanitize_input"}):
        # Very simplistic HTML tag remover
        sanitized = re.sub(r"<[^>]*>", "", input_string or "")

        logger.log_to_console("DEBUG", f"Input sanitized from '{input_string}' to '{sanitized}'.")
        return sanitized
