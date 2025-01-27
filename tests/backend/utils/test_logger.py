import logging
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError
import pytest
from backend.utils.logger import CentralizedLogger


@pytest.fixture
def logger_fixture():
    """Fixture to set up the centralized logger."""
    return CentralizedLogger("test_logger")


@pytest.mark.usefixtures("function_db_setup")
class TestLogger:
    """
    Tests for the CentralizedLogger class.
    """

    def test_logger_initialization(self, logger_fixture):
        assert isinstance(logger_fixture.logger, logging.Logger), \
            "CentralizedLogger should initialize a Logger instance."
        assert len(logger_fixture.logger.handlers) > 0, \
            "Logger should have at least one handler."
        handler = logger_fixture.logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler), \
            "The handler should be a StreamHandler."
        assert handler.formatter is not None, "The handler should have a formatter."
        # Default is DEBUG if no env var is set
        assert logger_fixture.logger.level == logging.DEBUG, \
            "Logger level should be set to DEBUG by default."

    def test_log_to_console(self, logger_fixture):
        with patch.object(logger_fixture.logger, "info") as mock_info:
            logger_fixture.log_to_console("INFO", "Test console log message.", context="TestContext")
            mock_info.assert_called_once_with(
                'Test console log message. | Context: {"context": "TestContext"}'
            )

        with patch.object(logger_fixture.logger, "error") as mock_error:
            logger_fixture.log_to_console("ERROR", "Error log message.")
            mock_error.assert_called_once_with("Error log message.")

    def test_invalid_log_level(self, logger_fixture):
        with patch.object(logger_fixture.logger, "warning") as mock_warning:
            logger_fixture.log_to_console("INVALID", "Test invalid log level.")
            mock_warning.assert_called_once_with(
                "Invalid log level '%s': %s", "INVALID", "Test invalid log level."
            )

    def test_log_to_db(self, logger_fixture):
        """
        Verifies log_to_db calls the DB session to add and commit
        a Log record, if the database is available.
        """
        with patch("backend.db.session.add") as mock_add, patch("backend.db.session.commit") as mock_commit:
            logger_fixture.log_to_db(
                level="DEBUG",
                message="Test DB log message",
                module="TestModule",
                user_id=1,
                meta_data={"key": "value"},
            )
            assert mock_add.called, "A log entry should be added to the session."
            assert mock_commit.called, "The session should be committed."

    def test_log_to_db_handles_exceptions(self, logger_fixture):
        """
        Verifies that database errors (SQLAlchemyError) are handled gracefully.
        """
        with patch("backend.db.session.add", side_effect=SQLAlchemyError("DB error")) as mock_add, \
             patch.object(logger_fixture.logger, "error") as mock_error, \
             patch("backend.db.session.rollback") as mock_rollback:
            logger_fixture.log_to_db(
                level="ERROR", message="Failing DB log message", module="TestModule"
            )
            assert mock_add.called, "The log entry attempt should be made."
            assert mock_rollback.called, "Session should be rolled back on error."
            mock_error.assert_called_once_with("Failed to log to database: %s", "DB error")

    def test_format_message(self, logger_fixture):
        formatted_message = logger_fixture.format_message("Base message", key1="value1", key2="value2")
        assert formatted_message == 'Base message | Context: {"key1": "value1", "key2": "value2"}', \
            "Should include JSON-encoded context."
        plain_message = logger_fixture.format_message("Plain message")
        assert plain_message == "Plain message", \
            "Should handle plain messages without context."
