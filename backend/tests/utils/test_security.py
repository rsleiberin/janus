# test_security.py

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

    def test_authentication_success(self):
        """
        Expect successful authentication when valid credentials are provided.
        """
        credentials = {"username": "admin", "password": "password"}
        assert check_authentication(credentials) is True

    def test_authentication_failure(self):
        """
        Expect an AuthenticationError when invalid credentials are provided.
        """
        credentials = {"username": "wrong", "password": "creds"}
        with pytest.raises(AuthenticationError) as exc_info:
            check_authentication(credentials)
        assert "Invalid username or password." in str(exc_info.value)

    def test_missing_credentials(self):
        """
        Expect an AuthenticationError when credentials are missing.
        """
        credentials = {"username": "admin"}  # No password
        with pytest.raises(AuthenticationError) as exc_info:
            check_authentication(credentials)
        assert "Missing credentials." in str(exc_info.value)

    def test_authorization_success(self):
        """
        Expect successful authorization for matching roles.
        """
        assert check_authorization("admin", "admin") is True

    def test_authorization_failure(self):
        """
        Expect an AuthorizationError when roles do not match.
        """
        with pytest.raises(AuthorizationError) as exc_info:
            check_authorization("user", "admin")
        assert "User role 'user' does not meet requirement 'admin'." in str(
            exc_info.value
        )

    def test_validate_input_success(self):
        """
        Validate acceptable input.
        """
        assert validate_input("ValidInput_123") is True

    def test_validate_input_failure(self):
        """
        Expect ValidationError when input does not match the default pattern.
        """
        with pytest.raises(ValidationError):
            validate_input("Invalid Input!")  # Contains space and punctuation

    def test_sanitize_input(self):
        """
        Verify that HTML tags are removed during sanitization.
        """
        raw_html = "<script>alert('Hack');</script>Hello"
        sanitized = sanitize_input(raw_html)
        assert "<script>" not in sanitized
        assert sanitized.endswith("Hello")
