import logging
import pytest
from unittest.mock import patch
from backend.utils.logger import CentralizedLogger


@pytest.fixture
def logger():
    """Fixture to set up the centralized logger."""
    return CentralizedLogger()


def test_logger_initialization(logger):
    """Test the initialization of the CentralizedLogger."""
    assert isinstance(
        logger.logger, logging.Logger
    ), "CentralizedLogger should initialize a Logger instance."
    assert len(logger.logger.handlers) > 0, "Logger should have at least one handler."
    handler = logger.logger.handlers[0]
    assert isinstance(
        handler, logging.StreamHandler
    ), "The handler should be a StreamHandler."
    assert handler.formatter is not None, "The handler should have a formatter."
    assert logger.logger.level == logging.DEBUG, "Logger level should be set to DEBUG."


def test_log_to_console(logger):
    """Test logging messages to the console."""
    with patch.object(logger.logger, "info") as mock_info:
        logger.log_to_console(
            "INFO", "Test console log message.", context="TestContext"
        )
        mock_info.assert_called_once_with(
            'Test console log message. | Context: {"context": "TestContext"}'
        )

    with patch.object(logger.logger, "error") as mock_error:
        logger.log_to_console("ERROR", "Error log message.")
        mock_error.assert_called_once_with("Error log message.")


def test_invalid_log_level(logger):
    """Test handling of invalid log levels."""
    with patch.object(logger.logger, "warning") as mock_warning:
        logger.log_to_console("INVALID", "Test invalid log level.")
        mock_warning.assert_called_once_with(
            "Invalid log level 'INVALID': Test invalid log level."
        )


def test_log_to_db(logger):
    """Test logging messages to the database."""
    with patch("backend.db.session.add") as mock_add, patch(
        "backend.db.session.commit"
    ) as mock_commit:
        logger.log_to_db(
            level="DEBUG",
            message="Test DB log message",
            module="TestModule",
            user_id=1,
            meta_data={"key": "value"},
        )
        assert mock_add.called, "The log entry should be added to the database session."
        assert mock_commit.called, "The database session should be committed."


def test_log_to_db_handles_exceptions(logger):
    """Test that database logging handles exceptions gracefully."""
    with patch(
        "backend.db.session.add", side_effect=Exception("DB error")
    ) as mock_add, patch.object(logger.logger, "error") as mock_error, patch(
        "backend.db.session.rollback"
    ) as mock_rollback:
        logger.log_to_db(
            level="ERROR", message="Failing DB log message", module="TestModule"
        )
        assert (
            mock_add.called
        ), "The log entry should attempt to be added to the database session."
        assert (
            mock_rollback.called
        ), "The database session should be rolled back on error."
        mock_error.assert_called_once_with("Failed to log to database: DB error")


def test_format_message(logger):
    """Test the message formatting function."""
    formatted_message = logger.format_message(
        "Base message", key1="value1", key2="value2"
    )
    assert (
        formatted_message
        == 'Base message | Context: {"key1": "value1", "key2": "value2"}'
    ), "Message formatting should include JSON-encoded context."
    plain_message = logger.format_message("Plain message")
    assert (
        plain_message == "Plain message"
    ), "Message formatting should handle plain messages without context."
