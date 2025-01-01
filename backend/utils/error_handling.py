# This module will handle standardized error handling across the backend, ensuring that error responses are consistent and meaningful.

def handle_db_error(error):
    """
    Standardizes database error responses.
    Args:
        error (Exception): The exception raised during the database operation.
    Returns:
        dict: The error message and a specific error code.
    """
    return {"error": "Database operation failed", "details": str(error)}, 500

def handle_not_found_error(resource_name):
    """
    Standardizes 'not found' error responses.
    Args:
        resource_name (str): The name of the resource that was not found.
    Returns:
        dict: The error message indicating resource was not found.
    """
    return {"error": f"{resource_name} not found"}, 404

def handle_general_error(error):
    """
    Standardizes general error responses.
    Args:
        error (Exception): The exception raised during the operation.
    Returns:
        dict: The error message for general errors.
    """
    return {"error": "An unexpected error occurred", "details": str(error)}, 500
