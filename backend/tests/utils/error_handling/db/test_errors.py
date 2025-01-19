import pytest
from sqlalchemy.exc import SQLAlchemyError
from backend.utils.error_handling.db.errors import (
    handle_database_error,
    DatabaseConnectionError,
    SchemaCreationError,
    SessionCommitError,
    UserError,
    AnalyticsError,
    ImageError,
    LogError,
    SecurityError,
    MultiModelError,
)

# Parameterized test data for handle_database_error
ERROR_TEST_CASES = [
    (
        DatabaseConnectionError("Connection failed"),
        "DB_CONNECTION_ERROR",
        "Failed to connect to the database.",
    ),
    (
        SchemaCreationError("Schema creation failed"),
        "SCHEMA_CREATION_ERROR",
        "Failed to create the database schema.",
    ),
    (
        SessionCommitError("Commit failed"),
        "SESSION_COMMIT_ERROR",
        "An error occurred while committing to the database.",
    ),
    (UserError("User error occurred"), "USER_ERROR", "A user-related error occurred."),
    (
        AnalyticsError("Analytics error occurred"),
        "ANALYTICS_ERROR",
        "An analytics-related error occurred.",
    ),
    (
        ImageError("Image error occurred"),
        "IMAGE_ERROR",
        "An image-related error occurred.",
    ),
    (LogError("Log error occurred"), "LOG_ERROR", "A log-related error occurred."),
    (
        SecurityError("Security error occurred"),
        "SECURITY_ERROR",
        "A security-related error occurred.",
    ),
    (
        MultiModelError("Multi-model error occurred"),
        "MULTI_MODEL_ERROR",
        "A multi-model-related error occurred.",
    ),
]


@pytest.mark.parametrize("error,expected_code,expected_message", ERROR_TEST_CASES)
def test_handle_database_error(
    error, expected_code, expected_message, function_db_setup
):
    """Test handle_database_error with various error types."""
    response, status = handle_database_error(
        error, module="test_module", meta_data={"test": "data"}
    )
    assert status == 500
    assert response["status"] == 500
    assert response["error_code"] == expected_code
    assert response["message"] == expected_message
    assert response["details"] == str(error)
    assert response["meta_data"] == {"test": "data"}


def test_handle_database_error_sqlalchemy_error(function_db_setup):
    """Test handle_database_error with SQLAlchemyError."""
    error = SQLAlchemyError("SQLAlchemy generic error")
    response, status = handle_database_error(
        error, module="test_module", meta_data={"test": "data"}
    )
    assert status == 500
    assert response["status"] == 500
    assert response["error_code"] == "SQLALCHEMY_ERROR"
    assert response["message"] == "A general database error occurred."
    assert response["details"] == str(error)
    assert response["meta_data"] == {"test": "data"}


def test_handle_database_error_unknown_error(function_db_setup):
    """Test handle_database_error with an unknown exception type."""

    class UnknownError(Exception):
        pass

    error = UnknownError("An unknown error occurred")
    response, status = handle_database_error(
        error, module="test_module", meta_data={"test": "data"}
    )
    assert status == 500
    assert response["status"] == 500
    assert response["error_code"] == "UNKNOWN_DB_ERROR"
    assert response["message"] == "An unknown database error occurred."
    assert response["details"] == str(error)
    assert response["meta_data"] == {"test": "data"}
