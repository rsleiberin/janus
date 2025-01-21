import pytest
from unittest.mock import patch
from backend.db import db
from backend.models import Admin
from backend.db.helpers.admin_helpers import AdminHelpers
from backend.utils.error_handling.db.errors import AdminNotFoundError


@pytest.mark.usefixtures("function_db_setup")
def test_create_admin():
    """
    Tests the creation of an Admin record using AdminHelpers.create
    and verifies the associated logging.
    """
    admin_data = {"user_id": 1, "admin_level": "superadmin"}

    with patch(
        "backend.utils.logger.CentralizedLogger.log_to_console"
    ) as mock_console_log:
        # Create admin
        admin = AdminHelpers.create(admin_data)

        # Verify admin creation
        assert admin is not None, "Admin creation failed."
        assert admin.user_id == admin_data["user_id"], "Admin user_id mismatch."
        assert admin.admin_level == admin_data["admin_level"], "Admin level mismatch."

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO", "Admin created successfully.", meta_data=admin_data
        )


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_id():
    """
    Tests retrieval of an Admin record by ID using AdminHelpers.get_by_id
    and verifies the associated logging.
    """
    admin_data = {"user_id": 1, "admin_level": "superadmin"}
    admin = AdminHelpers.create(admin_data)

    with patch(
        "backend.utils.logger.CentralizedLogger.log_to_console"
    ) as mock_console_log:
        fetched_admin = AdminHelpers.get_by_id(admin.id)

        # Verify admin retrieval
        assert fetched_admin is not None, "Admin not found by ID."
        assert fetched_admin.id == admin.id, "Admin ID mismatch."

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO", f"Admin retrieved successfully: ID {admin.id}."
        )


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_id_not_found():
    """
    Tests the behavior when trying to fetch a non-existent Admin record.
    """
    invalid_admin_id = 99999

    with patch(
        "backend.utils.logger.CentralizedLogger.log_to_console"
    ) as mock_console_log:
        with pytest.raises(AdminNotFoundError, match="Admin not found."):
            AdminHelpers.get_by_id(invalid_admin_id)

        # Verify logging
        mock_console_log.assert_called_with(
            "WARNING", f"Admin not found: ID {invalid_admin_id}."
        )


@pytest.mark.usefixtures("function_db_setup")
def test_delete_admin():
    """
    Tests deleting an Admin record using AdminHelpers.delete
    and verifies the associated logging.
    """
    admin_data = {"user_id": 1, "admin_level": "superadmin"}
    admin = AdminHelpers.create(admin_data)

    with patch(
        "backend.utils.logger.CentralizedLogger.log_to_console"
    ) as mock_console_log:
        AdminHelpers.delete(admin.id)

        # Verify deletion
        deleted_admin = db.session.get(Admin, admin.id)
        assert deleted_admin is None, "Admin was not deleted."

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO", f"Admin {admin.id} deleted successfully."
        )


@pytest.mark.usefixtures("function_db_setup")
def test_exists_admin():
    """
    Tests checking the existence of an Admin record by ID using AdminHelpers.exists
    and verifies the associated logging.
    """
    admin_data = {"user_id": 1, "admin_level": "superadmin"}
    admin = AdminHelpers.create(admin_data)

    with patch(
        "backend.utils.logger.CentralizedLogger.log_to_console"
    ) as mock_console_log:
        admin_exists = AdminHelpers.exists(admin.id)

        # Verify existence check
        assert admin_exists is True, "Admin existence check failed."

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO", f"Admin existence check for ID {admin.id}: {admin_exists}."
        )
