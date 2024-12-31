import pytest
import logging
from datetime import datetime
from backend import create_app
from backend.db import db
from backend.models import Admin  # Only import Admin, since User is not used in the AdminHelpers test file
from backend.db.helpers import AdminHelpers

# Setup console logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[logging.StreamHandler()])  # Log only to console
logger = logging.getLogger("test_logger")

# Test AdminHelpers class

def test_create_admin(init_db):
    admin_data = {
        "user_id": 1,  # Assuming we have a user with ID 1 in the test setup
        "admin_level": "superadmin"
    }
    app = create_app()
    with app.app_context():  # Ensure app context is properly set up
        admin = AdminHelpers.create(admin_data)
    assert admin.id is not None  # Ensure the admin has been created with an ID
    assert admin.admin_level == "superadmin"  # Ensure the admin level is correct


def test_get_by_id(init_db):
    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }
    app = create_app()
    with app.app_context():  # Ensure app context is properly set up
        admin = AdminHelpers.create(admin_data)
        fetched_admin = AdminHelpers.get_by_id(admin.id)
    assert fetched_admin.id == admin.id  # Ensure the correct admin is fetched


def test_get_by_user_id(init_db):
    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }
    app = create_app()
    with app.app_context():  # Ensure app context is properly set up
        admin = AdminHelpers.create(admin_data)
        fetched_admin = AdminHelpers.get_by_user_id(1)
    assert fetched_admin.user_id == 1  # Ensure the correct admin is fetched by user ID


def test_update_admin(init_db):
    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }
    app = create_app()
    with app.app_context():  # Ensure app context is properly set up
        admin = AdminHelpers.create(admin_data)
        updated_data = {"admin_level": "moderator"}
        updated_admin = AdminHelpers.update(admin.id, updated_data)
    assert updated_admin.admin_level == "moderator"  # Ensure the admin level is updated correctly


def test_delete_admin(init_db):
    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }
    app = create_app()
    with app.app_context():  # Ensure app context is properly set up
        admin = AdminHelpers.create(admin_data)
        AdminHelpers.delete(admin.id)
        deleted_admin = Admin.query.get(admin.id)
    assert deleted_admin is None  # Ensure the admin is deleted


def test_count_admins(init_db):
    admin_data_1 = {
        "user_id": 1,
        "admin_level": "superadmin"
    }
    admin_data_2 = {
        "user_id": 2,
        "admin_level": "moderator"
    }
    app = create_app()
    with app.app_context():  # Ensure app context is properly set up
        AdminHelpers.create(admin_data_1)
        AdminHelpers.create(admin_data_2)
        admin_count = AdminHelpers.count()
    assert admin_count == 2  # Ensure the admin count is correct


def test_exists_admin(init_db):
    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }
    app = create_app()
    with app.app_context():  # Ensure app context is properly set up
        admin = AdminHelpers.create(admin_data)
        admin_exists = AdminHelpers.exists(admin.id)
    assert admin_exists is True  # Ensure the admin exists
