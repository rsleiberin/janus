import pytest
from backend.db import db
from backend.db.helpers.security_helpers import SecurityHelpers
from backend.utils.logger import CentralizedLogger
from backend.models import Security
from backend.utils.error_handling.db.errors import (
    SecurityActionCreationError,
    SecurityEntryNotFoundError,
    SecurityQueryError,
    SecurityEntryDeletionError,
)

logger = CentralizedLogger("test_security_helpers")


@pytest.mark.usefixtures("function_db_setup")
def test_create_security_entry():
    logger.log_to_console("DEBUG", "Starting test_create_security_entry...")
    user_id = 1
    action = "login_attempt"

    # Test successful creation
    security_entry = SecurityHelpers.create_security_entry(user_id, action)
    assert security_entry.id is not None, "Security entry was not assigned an ID."
    assert security_entry.action == action, "Security entry action mismatch."
    assert security_entry.user_id == user_id, "Security entry user_id mismatch."

    # Test creation failure (invalid input)
    with pytest.raises(SecurityActionCreationError):
        SecurityHelpers.create_security_entry(None, action)

    logger.log_to_console("DEBUG", "test_create_security_entry passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_security_by_id():
    logger.log_to_console("DEBUG", "Starting test_get_security_by_id...")
    user_id = 1
    action = "login_attempt"

    security_entry = SecurityHelpers.create_security_entry(user_id, action)

    # Test successful retrieval
    fetched_security = SecurityHelpers.get_security_by_id(security_entry.id)
    assert fetched_security is not None, "Fetched security entry is None."
    assert fetched_security.id == security_entry.id, "Mismatch security entry ID."

    # Test failure for non-existent ID
    with pytest.raises(SecurityEntryNotFoundError, match="Security entry with ID 9999 not found."):
        SecurityHelpers.get_security_by_id(9999)

    logger.log_to_console("DEBUG", "test_get_security_by_id passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_security_by_user():
    logger.log_to_console("DEBUG", "Starting test_get_security_by_user...")
    user_id = 1
    SecurityHelpers.create_security_entry(user_id, "login_attempt")
    SecurityHelpers.create_security_entry(user_id, "password_change")

    # Test successful retrieval
    entries = SecurityHelpers.get_security_by_user(user_id)
    assert len(entries) == 2, "Expected 2 security entries for the user."

    # Test retrieval for a user with no entries
    entries = SecurityHelpers.get_security_by_user(9999)
    assert len(entries) == 0, "Expected no security entries for the user."

    logger.log_to_console("DEBUG", "test_get_security_by_user passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_recent_security_entries():
    logger.log_to_console("DEBUG", "Starting test_get_recent_security_entries...")
    user_id = 1
    SecurityHelpers.create_security_entry(user_id, "login_attempt")
    SecurityHelpers.create_security_entry(user_id, "password_change")

    # Test retrieving most recent entry
    recent = SecurityHelpers.get_recent_security_entries(limit=1)
    assert len(recent) == 1, "Expected 1 most recent security entry."
    assert recent[0].action == "password_change", "Most recent entry mismatch."

    # Test invalid limit
    with pytest.raises(SecurityQueryError, match="Limit must be a positive integer."):
        SecurityHelpers.get_recent_security_entries(limit=None)

    logger.log_to_console("DEBUG", "test_get_recent_security_entries passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_delete_security_entry():
    logger.log_to_console("DEBUG", "Starting test_delete_security_entry...")
    user_id = 1
    action = "login_attempt"

    security_entry = SecurityHelpers.create_security_entry(user_id, action)

    # Test successful deletion
    SecurityHelpers.delete_security_entry(security_entry.id)
    deleted = db.session.get(Security, security_entry.id)
    assert deleted is None, "Security entry still present after deletion."

    # Test deletion of non-existent entry
    with pytest.raises(SecurityEntryDeletionError):
        SecurityHelpers.delete_security_entry(9999)

    logger.log_to_console("DEBUG", "test_delete_security_entry passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_count_security_entries():
    logger.log_to_console("DEBUG", "Starting test_count_security_entries...")
    user_id = 1
    SecurityHelpers.create_security_entry(user_id, "login_attempt")
    SecurityHelpers.create_security_entry(user_id, "password_change")

    # Test successful count
    total = SecurityHelpers.count()
    assert total == 2, "Expected exactly 2 security entries."

    # Test count after deletion
    SecurityHelpers.delete_security_entry(1)
    total = SecurityHelpers.count()
    assert total == 1, "Expected exactly 1 security entry after deletion."

    logger.log_to_console("DEBUG", "test_count_security_entries passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_exists_security_entry():
    logger.log_to_console("DEBUG", "Starting test_exists_security_entry...")
    user_id = 1
    security_entry = SecurityHelpers.create_security_entry(user_id, "login_attempt")

    # Test existence of entry
    assert SecurityHelpers.exists(security_entry.id) is True, "Expected entry to exist."

    # Test non-existent entry
    assert SecurityHelpers.exists(9999) is False, "Expected entry to not exist."

    logger.log_to_console("DEBUG", "test_exists_security_entry passed successfully.")
