# File: backend/tests/db/helpers/test_user_helpers.py

import pytest
from backend.db import db
from backend.db.helpers.user_helpers import UserHelpers
from backend.models import User
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.exceptions import GeneralError

logger = CentralizedLogger("test_user_helpers")

@pytest.mark.usefixtures("function_db_setup")
def test_create_user():
    logger.log_to_console("DEBUG", "Starting test_create_user...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password_hash": "somehash",
    }
    new_user = UserHelpers.create(user_data)
    assert new_user.id is not None, "User was not assigned an ID."
    assert new_user.username == "testuser", "Username mismatch."
    logger.log_to_console("DEBUG", "test_create_user passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_id():
    logger.log_to_console("DEBUG", "Starting test_get_by_id...")
    user_data = {
        "username": "getbyid_user",
        "email": "getbyid@example.com",
        "password_hash": "hash123",
    }
    created_user = UserHelpers.create(user_data)
    db.session.flush()

    # Test successful fetch
    fetched_user = UserHelpers.get_by_id(created_user.id)
    assert fetched_user is not None, "Fetched user is None."
    assert fetched_user.id == created_user.id, "Fetched ID does not match created user."

    # Test failure for non-existent ID
    with pytest.raises(GeneralError) as exc_info:
        UserHelpers.get_by_id(9999)
    assert "An error occurred in user_helpers: User with ID 9999 not found." in str(exc_info.value)

    logger.log_to_console("DEBUG", "test_get_by_id passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_email():
    logger.log_to_console("DEBUG", "Starting test_get_by_email...")
    user_data = {
        "username": "email_user",
        "email": "emailtest@example.com",
        "password_hash": "abc123",
    }
    created_user = UserHelpers.create(user_data)

    # Test successful fetch
    fetched_by_email = UserHelpers.get_by_email("emailtest@example.com")
    assert fetched_by_email is not None, "Expected to find a user by email."
    assert fetched_by_email.id == created_user.id, "Email-based fetch mismatch."

    # Test failure for non-existent email
    with pytest.raises(GeneralError) as exc_info:
        UserHelpers.get_by_email("nonexistent@example.com")
    assert "An error occurred in user_helpers: User with email nonexistent@example.com not found." in str(exc_info.value)

    logger.log_to_console("DEBUG", "test_get_by_email passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_update_user():
    logger.log_to_console("DEBUG", "Starting test_update_user...")
    user_data = {
        "username": "updateuser",
        "email": "update@example.com",
        "password_hash": "oldhash",
    }
    created_user = UserHelpers.create(user_data)
    updated_data = {"username": "updateduser", "password_hash": "newhash"}

    updated_user = UserHelpers.update(created_user.id, updated_data)
    assert updated_user.username == "updateduser", "Username not updated correctly."
    assert updated_user.password_hash == "newhash", "Password hash not updated."
    logger.log_to_console("DEBUG", "test_update_user passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_delete_user():
    logger.log_to_console("DEBUG", "Starting test_delete_user...")
    user_data = {
        "username": "deleteuser",
        "email": "delete@example.com",
        "password_hash": "deletehash",
    }
    created_user = UserHelpers.create(user_data)
    user_id = created_user.id

    # Test successful deletion
    UserHelpers.delete(user_id)

    with pytest.raises(GeneralError) as exc_info:
        UserHelpers.get_by_id(user_id)
    assert f"An error occurred in user_helpers: User with ID {user_id} not found." in str(exc_info.value)

    logger.log_to_console("DEBUG", "test_delete_user passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_count_users():
    logger.log_to_console("DEBUG", "Starting test_count_users...")
    user_data_1 = {
        "username": "countuser1",
        "email": "count1@example.com",
        "password_hash": "hash1",
    }
    user_data_2 = {
        "username": "countuser2",
        "email": "count2@example.com",
        "password_hash": "hash2",
    }
    UserHelpers.create(user_data_1)
    UserHelpers.create(user_data_2)

    total_users = UserHelpers.count()
    assert total_users == 2, f"Expected 2 users, found {total_users}."
    logger.log_to_console("DEBUG", "test_count_users passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_exists_user():
    logger.log_to_console("DEBUG", "Starting test_exists_user...")
    user_data = {
        "username": "existsuser",
        "email": "exists@example.com",
        "password_hash": "exists_hash",
    }
    new_user = UserHelpers.create(user_data)
    user_exists = UserHelpers.exists(new_user.id)
    assert user_exists is True, "Expected the user to exist."
    logger.log_to_console("DEBUG", "test_exists_user passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_user_query_error():
    logger.log_to_console("DEBUG", "Starting test_user_query_error...")

    # Simulate a query error by deliberately causing an invalid SQLAlchemy query using the helper method
    with pytest.raises(GeneralError) as exc_info:
        UserHelpers.get_user_by_nonexistent_field("value")
    
    assert "An error occurred in user_helpers: Entity namespace for \"users\" has no property \"nonexistent_field\"" in str(exc_info.value)

    logger.log_to_console("DEBUG", "test_user_query_error passed successfully.")
