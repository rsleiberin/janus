import pytest
from backend.utils.security import (
    check_authentication,
    check_authorization,
    validate_input,
    sanitize_input,
)
from backend.utils.error_handling.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ValidationError,
)


@pytest.mark.usefixtures("function_db_setup")
class TestSecurity:
    """
    Tests for the security module (authentication, authorization, validation).
    """

    def test_authentication_success(self):
        credentials = {"username": "admin", "password": "password"}
        assert check_authentication(credentials) is True, \
            "Valid credentials should pass authentication."

    def test_authentication_failure(self):
        credentials = {"username": "wrong", "password": "creds"}
        with pytest.raises(AuthenticationError) as exc_info:
            check_authentication(credentials)
        assert "Invalid username or password." in str(exc_info.value), \
            "Wrong credentials should raise AuthenticationError."

    def test_missing_credentials(self):
        credentials = {"username": "admin"}  # No password
        with pytest.raises(AuthenticationError) as exc_info:
            check_authentication(credentials)
        assert "Missing credentials." in str(exc_info.value), \
            "Missing password should raise AuthenticationError."

    def test_authorization_success(self):
        assert check_authorization("admin", "admin") is True, \
            "Matching roles should pass authorization."

    def test_authorization_failure(self):
        with pytest.raises(AuthorizationError) as exc_info:
            check_authorization("user", "admin")
        assert "User role 'user' does not meet requirement 'admin'." in str(exc_info.value), \
            "Non-matching roles should raise AuthorizationError."

    def test_validate_input_success(self):
        assert validate_input("ValidInput_123") is True, \
            "Input that matches the default pattern should validate successfully."

    def test_validate_input_failure(self):
        with pytest.raises(ValidationError):
            validate_input("Invalid Input!")  # Contains space and punctuation

    def test_sanitize_input(self):
        raw_html = "<script>alert('Hack');</script>Hello"
        sanitized = sanitize_input(raw_html)
        assert "<script>" not in sanitized, "HTML tags should be removed."
        assert sanitized.endswith("Hello"), "Text after HTML tags should remain."

