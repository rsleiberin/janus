import pytest
from backend.utils.error_handling.exceptions import (
    FileHandlerError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    DatabaseConnectionError,
    SchemaCreationError,
    SessionCommitError,
    LogNotFoundError,
    GeneralError,
    HealthCheckError,
    SecurityError,
    ImageError,
)


@pytest.mark.usefixtures("function_db_setup")
class TestCustomExceptions:
    """
    Basic coverage to ensure each custom exception can be raised and captured.
    """

    def test_file_handler_error(self):
        with pytest.raises(FileHandlerError, match="A file handler error"):
            raise FileHandlerError("A file handler error")

    def test_authentication_error(self):
        with pytest.raises(AuthenticationError, match="Invalid credentials"):
            raise AuthenticationError("Invalid credentials")

    def test_authorization_error(self):
        with pytest.raises(AuthorizationError, match="Insufficient privileges"):
            raise AuthorizationError("Insufficient privileges")

    def test_validation_error(self):
        with pytest.raises(ValidationError, match="Bad input"):
            raise ValidationError("Bad input")

    def test_database_connection_error(self):
        with pytest.raises(DatabaseConnectionError, match="DB conn problem"):
            raise DatabaseConnectionError("DB conn problem")

    def test_schema_creation_error(self):
        with pytest.raises(SchemaCreationError, match="Schema error"):
            raise SchemaCreationError("Schema error")

    def test_session_commit_error(self):
        with pytest.raises(SessionCommitError, match="Commit failed"):
            raise SessionCommitError("Commit failed")

    def test_log_not_found_error(self):
        with pytest.raises(LogNotFoundError, match="No log entry"):
            raise LogNotFoundError("No log entry")

    def test_general_error(self):
        with pytest.raises(GeneralError, match="Generic error"):
            raise GeneralError("Generic error")

    def test_health_check_error(self):
        with pytest.raises(HealthCheckError, match="Health check failed"):
            raise HealthCheckError("Health check failed")

    def test_security_error(self):
        with pytest.raises(SecurityError, match="Security issue"):
            raise SecurityError("Security issue")

    def test_image_error(self):
        with pytest.raises(ImageError, match="Image error"):
            raise ImageError("Image error")