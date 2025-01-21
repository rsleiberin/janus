# File: backend/tests/utils/error_handling/test_error_handling.py

import pytest
from backend.utils.error_handling.error_handling import (
    format_error_response,
    log_error,
    handle_general_error,
    handle_http_error,
    ErrorContext,
)
from backend.utils.error_handling.utils.errors import FileHandlerError


def test_format_error_response():
    """Test the format_error_response function."""
    response = format_error_response(
        status=400,
        error_code="BAD_REQUEST",
        message="Invalid input",
        details="Field 'email' is required",
        meta_data={"field": "email"},
    )
    assert response == {
        "status": 400,
        "error_code": "BAD_REQUEST",
        "message": "Invalid input",
        "details": "Field 'email' is required",
        "meta_data": {"field": "email"},
    }


@pytest.mark.usefixtures("function_db_setup")
def test_log_error(app):
    """Test the log_error function."""
    with app.app_context():
        with pytest.raises(FileHandlerError, match="Test error"):
            try:
                raise ValueError("Test error")
            except ValueError as e:
                log_error(e, module="test_module", user_id=42, meta_data={"action": "test"})
                raise FileHandlerError("Test error") from e
        # Ensure no unhandled exceptions are raised.


@pytest.mark.usefixtures("function_db_setup")
def test_handle_general_error(app):
    """Test the handle_general_error function."""
    with app.app_context():
        try:
            raise ValueError("Something went wrong!")
        except ValueError as e:
            response, status = handle_general_error(e, meta_data={"info": "test"})
            assert status == 500
            assert response["status"] == 500
            assert response["error_code"] == "GENERAL_ERROR"
            assert response["message"] == "An unexpected error occurred."
            assert response["details"] == "Something went wrong!"
            assert response["meta_data"] == {"info": "test"}


@pytest.mark.usefixtures("function_db_setup")
def test_handle_http_error():
    """Test the handle_http_error function."""
    response, status = handle_http_error(
        status=404,
        error_code="NOT_FOUND",
        message="Resource not found",
        meta_data={"endpoint": "/api/resource"},
    )
    assert status == 404
    assert response["status"] == 404
    assert response["error_code"] == "NOT_FOUND"
    assert response["message"] == "Resource not found"
    assert response["meta_data"] == {"endpoint": "/api/resource"}


@pytest.mark.usefixtures("function_db_setup")
def test_error_context(app):
    """Test the ErrorContext manager."""
    with app.app_context():
        with pytest.raises(ValueError, match="This is a test error"):
            with ErrorContext(
                module="test_context", user_id=42, meta_data={"test": "data"}
            ):
                raise ValueError("This is a test error")
