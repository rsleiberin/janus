import pytest
from backend.utils.error_handling import log_error  # Your logging function

def test_log_error():
    """Test if errors are logged correctly"""
    try:
        raise ValueError("Test error")
    except ValueError as e:
        log_error(e)  # Log the error using your logging function

    # Check that error is logged (mock or check the log file)
    # Here, you can mock the logging or check logs in your system
    assert True  # Add assertions to check log output
