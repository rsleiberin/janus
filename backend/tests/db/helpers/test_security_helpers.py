import pytest
from backend.db import db
from backend.db.helpers.security_helpers import SecurityHelpers
from backend.utils.logger import CentralizedLogger
from backend.models import Security

logger = CentralizedLogger("test_security_helpers")

@pytest.mark.usefixtures("function_db_setup")
def test_create_security_entry():
    logger.log_to_console("DEBUG", "Starting test_create_security_entry...")
    user_id = 1
    action = "login_attempt"
    security_entry = SecurityHelpers.create_security_entry(user_id, action)
    assert security_entry.id is not None, "Security entry was not assigned an ID."
    assert security_entry.action == action, "Security entry action mismatch."
    assert security_entry.user_id == user_id, "Security entry user_id mismatch."
    logger.log_to_console("DEBUG", "test_create_security_entry passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_get_security_by_id():
    logger.log_to_console("DEBUG", "Starting test_get_security_by_id...")
    user_id = 1
    action = "login_attempt"
    security_entry = SecurityHelpers.create_security_entry(user_id, action)
    db.session.flush()

    fetched_security = SecurityHelpers.get_security_by_id(security_entry.id)
    assert fetched_security is not None, "Fetched security entry is None."
    assert fetched_security.id == security_entry.id, "Mismatch security entry ID."
    logger.log_to_console("DEBUG", "test_get_security_by_id passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_get_security_by_user():
    logger.log_to_console("DEBUG", "Starting test_get_security_by_user...")
    user_id = 1
    action = "login_attempt"
    SecurityHelpers.create_security_entry(user_id, action)
    entries = SecurityHelpers.get_security_by_user(user_id)
    assert len(entries) > 0, "Expected security entries for the user."
    logger.log_to_console("DEBUG", "test_get_security_by_user passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_get_recent_security_entries():
    logger.log_to_console("DEBUG", "Starting test_get_recent_security_entries...")
    user_id = 1
    SecurityHelpers.create_security_entry(user_id, "login_attempt")
    SecurityHelpers.create_security_entry(user_id, "password_change")
    recent = SecurityHelpers.get_recent_security_entries(limit=1)
    assert len(recent) == 1, "Expected 1 most recent security entry."
    logger.log_to_console("DEBUG", "test_get_recent_security_entries passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_delete_security_entry():
    logger.log_to_console("DEBUG", "Starting test_delete_security_entry...")
    user_id = 1
    action = "login_attempt"
    security_entry = SecurityHelpers.create_security_entry(user_id, action)
    SecurityHelpers.delete_security_entry(security_entry.id)
    deleted = db.session.get(Security, security_entry.id)
    assert deleted is None, "Security entry still present after deletion."
    logger.log_to_console("DEBUG", "test_delete_security_entry passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_count_security_entries():
    logger.log_to_console("DEBUG", "Starting test_count_security_entries...")
    user_id = 1
    SecurityHelpers.create_security_entry(user_id, "login_attempt")
    total = SecurityHelpers.count()
    assert total == 1, "Expected exactly 1 security entry."
    logger.log_to_console("DEBUG", "test_count_security_entries passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_exists_security_entry():
    logger.log_to_console("DEBUG", "Starting test_exists_security_entry...")
    user_id = 1
    security_entry = SecurityHelpers.create_security_entry(user_id, "login_attempt")
    assert SecurityHelpers.exists(security_entry.id) is True, "Expected entry to exist."
    logger.log_to_console("DEBUG", "test_exists_security_entry passed successfully.")
