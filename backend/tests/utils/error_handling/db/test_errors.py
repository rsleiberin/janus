import pytest
from sqlalchemy.exc import SQLAlchemyError
from backend.utils.error_handling.db.errors import handle_database_error
from backend.utils.error_handling.error_handling import format_error_response

# Parameterized test data for handle_database_error
ERROR_TEST_CASES = [
    ("DatabaseConnectionError", "DB_CONNECTION_ERROR", "Failed to connect to the database."),
    ("SchemaCreationError", "SCHEMA_CREATION_ERROR", "Error creating database schema."),
    ("SessionCommitError", "SESSION_COMMIT_ERROR", "Failed to commit database session."),
    ("UserError", "USER_ERROR", "A user-related error occurred."),
    ("AnalyticsError", "ANALYTICS_ERROR", "An analytics-related error occurred."),
    ("ImageError", "IMAGE_ERROR", "An image-related error occurred."),
    ("LogError", "LOG_ERROR", "A log-related error occurred."),
    ("SecurityError", "SECURITY_ERROR", "A security-related error occurred."),
    ("UnknownError", "UNKNOWN_DB_ERROR", "An unknown database error occurred."),
]

@pytest.mark.parametrize("error_name, expected_code, expected_message", ERROR_TEST_CASES)
def test_handle_database_error(error_name, expected_code, expected_message):
    """Test handle_database_error with various error types."""
    # Dynamically create exception classes for testing
    error_class = type(error_name, (Exception,), {})
    error_instance = error_class(expected_message)

    response, status = handle_database_error(
        error_instance,
        module="test_module",
        meta_data={"test": "data"}
    )

    # Assertions for the response
    assert status == 500, "Expected HTTP status code 500"
    assert response["status"] == 500, "Expected response status 500"
    assert response["error_code"] == expected_code, f"Expected error code {expected_code}"
    assert response["message"] == expected_message, f"Expected message {expected_message}"
    assert response["details"] == str(error_instance), "Details should match the exception message"
    assert response["meta_data"] == {"test": "data"}, "Meta data mismatch"


def test_handle_database_error_sqlalchemy_error():
    """Test handle_database_error with SQLAlchemyError."""
    error = SQLAlchemyError("SQLAlchemy generic error")

    response, status = handle_database_error(
        error,
        module="test_module",
        meta_data={"test": "data"}
    )

    # Assertions for SQLAlchemyError
    assert status == 500, "Expected HTTP status code 500"
    assert response["status"] == 500, "Expected response status 500"
    assert response["error_code"] == "SQLALCHEMY_ERROR", "Expected SQLALCHEMY_ERROR code"
    assert response["message"] == "An unexpected database error occurred.", "Message mismatch"
    assert response["details"] == str(error), "Details should match the exception message"
    assert response["meta_data"] == {"test": "data"}, "Meta data mismatch"


def test_handle_database_error_unknown_error():
    """Test handle_database_error with an unknown exception type."""
    class UnknownError(Exception):
        """Custom exception for testing."""
        pass

    error = UnknownError("An unknown error occurred")

    response, status = handle_database_error(
        error,
        module="test_module",
        meta_data={"test": "data"}
    )

    # Assertions for unknown error
    assert status == 500, "Expected HTTP status code 500"
    assert response["status"] == 500, "Expected response status 500"
    assert response["error_code"] == "UNKNOWN_DB_ERROR", "Expected UNKNOWN_DB_ERROR code"
    assert response["message"] == "An unknown database error occurred.", "Message mismatch"
    assert response["details"] == str(error), "Details should match the exception message"
    assert response["meta_data"] == {"test": "data"}, "Meta data mismatch"
