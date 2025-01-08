import pytest
from backend.utils.error_handling.error_handling import (
    format_error_response, log_error, handle_general_error
)
from backend.utils.logger import CentralizedLogger

@pytest.fixture(scope="module")
def test_logger():
    """
    Provides a test-specific logger instance.
    """
    return CentralizedLogger("test_logger")

def test_format_error_response():
    """
    Tests the format_error_response function.
    """
    response = format_error_response(
        status=500,
        error_code="TEST_ERROR",
        message="This is a test error.",
        details="Details about the test error.",
        meta_data={"request_id": "12345"}
    )

    assert response["status"] == 500
    assert response["error_code"] == "TEST_ERROR"
    assert response["message"] == "This is a test error."
    assert response.get("details") == "Details about the test error."
    assert response.get("meta_data") == {"request_id": "12345"}

def test_log_error(test_logger, app, caplog):
    """
    Tests the log_error function.
    """
    with app.app_context():
        with caplog.at_level("ERROR"):
            log_error(
                error=Exception("Test exception"),
                module="test_module",
                user_id=42,
                meta_data={"key": "value"}
            )

        # Assert the log contains the correct information
        assert "Test exception" in caplog.text
        assert "test_module" in caplog.text
        assert "value" in caplog.text

def test_handle_general_error(app, caplog):
    """
    Tests the handle_general_error function.
    """
    with app.app_context():
        with caplog.at_level("ERROR"):
            response, status = handle_general_error(
                error=Exception("General test error"),
                meta_data={"key": "value"}
            )

        # Assert the response structure
        assert status == 500
        assert response["status"] == 500
        assert response["error_code"] == "GENERAL_ERROR"
        assert response["message"] == "An unexpected error occurred."
        assert response["details"] == "General test error"
        assert response["meta_data"] == {"key": "value"}

        # Assert the log contains the error message
        assert "General test error" in caplog.text
        assert "value" in caplog.text
