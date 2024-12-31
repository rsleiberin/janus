import pytest
import logging
from datetime import datetime
from backend import create_app
from backend.db import db
from backend.models import Image, User, Admin, Log, Analytics, Security
from backend.db.db_helpers import ImageHelpers, UserHelpers, AdminHelpers, LogHelpers, AnalyticsHelpers, SecurityHelpers

# Setup console logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[logging.StreamHandler()])  # Log only to console
logger = logging.getLogger("test_logger")


# Setup a test database
@pytest.fixture(scope="function")
def init_db():
    """Fixture to setup a clean test database for each test."""
    app = create_app()

    logger.debug("Creating app and setting up the database...")
    
    with app.app_context():
        # Verify if app context is properly set
        logger.debug(f"App context set: {app.app_context() is not None}")
        
        # Check if db is correctly initialized and if the tables exist
        logger.debug("Attempting to create all tables in the database.")
        try:
            db.create_all()  # Ensure tables are created within the app context
            logger.debug("Database initialized for testing.")
            print("Database initialized for testing.")
        except Exception as e:
            logger.error(f"Error during database setup: {e}")
            print(f"Error during database setup: {e}")
            raise  # Reraise exception to ensure the test fails

    yield
    
    # Cleanup after the test
    with app.app_context():
        try:
            logger.debug("Cleaning up the database...")
            print("Cleaning up the database...")
            db.session.remove()
            db.drop_all()  # Drop all tables after test
            logger.debug("Database cleaned up after test.")
            print("Database cleaned up after test.")
        except Exception as e:
            logger.error(f"Error during database cleanup: {e}")
            print(f"Error during database cleanup: {e}")
            raise  # Reraise exception to ensure the test fails


# Test ImageHelpers class

# Test for creating a new image
def test_create_image(init_db):
    image_data = {
        "filename": "test_image_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + ".jpg",  # Ensure unique filename
        "width": 800,
        "height": 600,
        "bit_depth": 24,
        "color_type": "RGB",
        "compression_method": "JPEG",
        "image_metadata": {"camera": "Canon", "lens": "50mm"},
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    
    # Wrapping helper function inside app context
    with create_app().app_context():
        image = ImageHelpers.create(image_data)
    
    assert image.id is not None  # Ensure the image has been created with an ID
    assert image.filename.startswith("test_image_")  # Ensure the filename is correct

# Test for retrieving an image by ID
def test_get_by_id(init_db):
    image_data = {
        "filename": "test_image.jpg",
        "width": 800,
        "height": 600,
        "bit_depth": 24,
        "color_type": "RGB",
        "compression_method": "JPEG",
        "image_metadata": {"camera": "Canon", "lens": "50mm"},
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    image = ImageHelpers.create(image_data)
    fetched_image = ImageHelpers.get_by_id(image.id)
    assert fetched_image.id == image.id  # Ensure the correct image is fetched

# Test for updating an image
def test_update_image(init_db):
    image_data = {
        "filename": "test_image.jpg",
        "width": 800,
        "height": 600,
        "bit_depth": 24,
        "color_type": "RGB",
        "compression_method": "JPEG",
        "image_metadata": {"camera": "Canon", "lens": "50mm"},
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    image = ImageHelpers.create(image_data)
    updated_data = {"width": 1024, "height": 768}
    updated_image = ImageHelpers.update(image.id, updated_data)
    assert updated_image.width == 1024
    assert updated_image.height == 768

# Test for deleting an image
def test_delete_image(init_db):
    image_data = {
        "filename": "test_image.jpg",
        "width": 800,
        "height": 600,
        "bit_depth": 24,
        "color_type": "RGB",
        "compression_method": "JPEG",
        "image_metadata": {"camera": "Canon", "lens": "50mm"},
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    image = ImageHelpers.create(image_data)
    ImageHelpers.delete(image.id)
    deleted_image = Image.query.get(image.id)
    assert deleted_image is None  # Ensure the image is deleted

# Test UserHelpers class

# Test for creating a new user
def test_create_user(init_db):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password_hash": "hashedpassword",
        "role": "user",
    }
    user = UserHelpers.create(user_data)
    assert user.id is not None  # Ensure the user has been created with an ID
    assert user.username == "testuser"  # Ensure the username is correct
    assert user.email == "testuser@example.com"  # Ensure the email is correct

# Test for retrieving a user by ID
def test_get_by_id(init_db):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password_hash": "hashedpassword",
        "role": "user",
    }
    user = UserHelpers.create(user_data)
    fetched_user = UserHelpers.get_by_id(user.id)
    assert fetched_user.id == user.id  # Ensure the correct user is fetched

# Test for retrieving a user by email
def test_get_by_email(init_db):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password_hash": "hashedpassword",
        "role": "user",
    }
    user = UserHelpers.create(user_data)
    fetched_user = UserHelpers.get_by_email("testuser@example.com")
    assert fetched_user.email == "testuser@example.com"  # Ensure the correct user is fetched by email

# Test for updating a user
def test_update_user(init_db):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password_hash": "hashedpassword",
        "role": "user",
    }
    user = UserHelpers.create(user_data)
    updated_data = {"role": "admin"}
    updated_user = UserHelpers.update(user.id, updated_data)
    assert updated_user.role == "admin"  # Ensure the role is updated correctly

# Test for deleting a user
def test_delete_user(init_db):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password_hash": "hashedpassword",
        "role": "user",
    }
    user = UserHelpers.create(user_data)
    UserHelpers.delete(user.id)
    deleted_user = User.query.get(user.id)
    assert deleted_user is None  # Ensure the user is deleted

# Test for counting the number of users
def test_count_users(init_db):
    user_data_1 = {
        "username": "testuser1",
        "email": "testuser1@example.com",
        "password_hash": "hashedpassword",
        "role": "user",
    }
    user_data_2 = {
        "username": "testuser2",
        "email": "testuser2@example.com",
        "password_hash": "hashedpassword",
        "role": "user",
    }
    UserHelpers.create(user_data_1)
    UserHelpers.create(user_data_2)
    user_count = UserHelpers.count()
    assert user_count == 2  # Ensure the user count is correct

# Test for checking if a user exists by ID
def test_exists_user(init_db):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password_hash": "hashedpassword",
        "role": "user",
    }
    user = UserHelpers.create(user_data)
    user_exists = UserHelpers.exists(user.id)
    assert user_exists is True  # Ensure the user exists

# Admin Model Helpers Tests

# Test for creating an admin
def test_create_admin(init_db):
    admin_data = {
        "user_id": 1,  # Assuming we have a user with ID 1 in the test setup
        "admin_level": "superadmin"
    }
    admin = AdminHelpers.create(admin_data)
    assert admin.id is not None  # Ensure the admin has been created with an ID
    assert admin.admin_level == "superadmin"  # Ensure the admin level is correct

# Test for retrieving an admin by ID
def test_get_by_id_admin(init_db):
    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }
    admin = AdminHelpers.create(admin_data)
    fetched_admin = AdminHelpers.get_by_id(admin.id)
    assert fetched_admin.id == admin.id  # Ensure the correct admin is fetched

# Test for retrieving an admin by user ID
def test_get_by_user_id_admin(init_db):
    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }
    admin = AdminHelpers.create(admin_data)
    fetched_admin = AdminHelpers.get_by_user_id(1)
    assert fetched_admin.user_id == 1  # Ensure the correct admin is fetched by user ID

# Test for updating an admin
def test_update_admin(init_db):
    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }
    admin = AdminHelpers.create(admin_data)
    updated_data = {"admin_level": "moderator"}
    updated_admin = AdminHelpers.update(admin.id, updated_data)
    assert updated_admin.admin_level == "moderator"  # Ensure the admin level is updated

# Test for deleting an admin
def test_delete_admin(init_db):
    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }
    admin = AdminHelpers.create(admin_data)
    AdminHelpers.delete(admin.id)
    deleted_admin = Admin.query.get(admin.id)
    assert deleted_admin is None  # Ensure the admin is deleted

# Test for counting the number of admins
def test_count_admins(init_db):
    admin_data_1 = {
        "user_id": 1,
        "admin_level": "superadmin"
    }
    admin_data_2 = {
        "user_id": 2,
        "admin_level": "moderator"
    }
    AdminHelpers.create(admin_data_1)
    AdminHelpers.create(admin_data_2)
    admin_count = AdminHelpers.count()
    assert admin_count == 2  # Ensure the admin count is correct

# Test for checking if an admin exists by ID
def test_exists_admin(init_db):
    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }
    admin = AdminHelpers.create(admin_data)
    admin_exists = AdminHelpers.exists(admin.id)
    assert admin_exists is True  # Ensure the admin exists


# Log Model Helpers Tests

# Test for creating a log
def test_create_log(init_db):
    log_data = {
        "action": "file uploaded",
        "user_id": 1  # Assuming we have a user with ID 1 in the test setup
    }
    log = LogHelpers.create_log(log_data["action"], log_data["user_id"])
    assert log.id is not None  # Ensure the log has been created with an ID
    assert log.action == "file uploaded"  # Ensure the action is correct

# Test for retrieving a log by ID
def test_get_by_id_log(init_db):
    log_data = {
        "action": "file uploaded",
        "user_id": 1
    }
    log = LogHelpers.create_log(log_data["action"], log_data["user_id"])
    fetched_log = LogHelpers.get_by_id(log.id)
    assert fetched_log.id == log.id  # Ensure the correct log is fetched

# Test for retrieving logs by user ID
def test_get_by_user_id_log(init_db):
    log_data_1 = {
        "action": "file uploaded",
        "user_id": 1
    }
    log_data_2 = {
        "action": "file deleted",
        "user_id": 1
    }
    LogHelpers.create_log(log_data_1["action"], log_data_1["user_id"])
    LogHelpers.create_log(log_data_2["action"], log_data_2["user_id"])
    logs = LogHelpers.get_by_user_id(1)
    assert len(logs) == 2  # Ensure that we get two logs for the same user

# Test for retrieving the most recent logs
def test_get_recent_logs(init_db):
    log_data_1 = {
        "action": "file uploaded",
        "user_id": 1
    }
    log_data_2 = {
        "action": "file deleted",
        "user_id": 2
    }
    LogHelpers.create_log(log_data_1["action"], log_data_1["user_id"])
    LogHelpers.create_log(log_data_2["action"], log_data_2["user_id"])
    recent_logs = LogHelpers.get_recent_logs(limit=1)
    assert len(recent_logs) == 1  # Ensure we get only one recent log

# Test for deleting a log
def test_delete_log(init_db):
    log_data = {
        "action": "file uploaded",
        "user_id": 1
    }
    log = LogHelpers.create_log(log_data["action"], log_data["user_id"])
    LogHelpers.delete_log(log.id)
    deleted_log = Log.query.get(log.id)
    assert deleted_log is None  # Ensure the log is deleted

# Test for counting the total number of logs
def test_count_logs(init_db):
    log_data_1 = {
        "action": "file uploaded",
        "user_id": 1
    }
    log_data_2 = {
        "action": "file deleted",
        "user_id": 2
    }
    LogHelpers.create_log(log_data_1["action"], log_data_1["user_id"])
    LogHelpers.create_log(log_data_2["action"], log_data_2["user_id"])
    log_count = LogHelpers.count()
    assert log_count == 2  # Ensure the log count is correct

# Test for checking if a log exists
def test_exists_log(init_db):
    log_data = {
        "action": "file uploaded",
        "user_id": 1
    }
    log = LogHelpers.create_log(log_data["action"], log_data["user_id"])
    log_exists = LogHelpers.exists(log.id)
    assert log_exists is True  # Ensure the log exists
# Analytics Model Helpers Tests

# Test for creating analytics
def test_create_analytics(init_db):
    analytics_data = {
        "data": {"key": "value"}  # Sample data for analytics
    }
    analytics = AnalyticsHelpers.create_analytics(analytics_data["data"])
    assert analytics.id is not None  # Ensure the analytics entry has been created with an ID
    assert analytics.data == {"key": "value"}  # Ensure the data is correct

# Test for retrieving analytics by ID
def test_get_by_id_analytics(init_db):
    analytics_data = {
        "data": {"key": "value"}
    }
    analytics = AnalyticsHelpers.create_analytics(analytics_data["data"])
    fetched_analytics = AnalyticsHelpers.get_by_id(analytics.id)
    assert fetched_analytics.id == analytics.id  # Ensure the correct analytics is fetched

# Test for retrieving all analytics entries
def test_get_all_analytics(init_db):
    analytics_data_1 = {
        "data": {"key": "value1"}
    }
    analytics_data_2 = {
        "data": {"key": "value2"}
    }
    AnalyticsHelpers.create_analytics(analytics_data_1["data"])
    AnalyticsHelpers.create_analytics(analytics_data_2["data"])
    all_analytics = AnalyticsHelpers.get_all_analytics()
    assert len(all_analytics) == 2  # Ensure all analytics entries are fetched

# Test for retrieving the most recent analytics entries
def test_get_recent_analytics(init_db):
    analytics_data_1 = {
        "data": {"key": "value1"}
    }
    analytics_data_2 = {
        "data": {"key": "value2"}
    }
    AnalyticsHelpers.create_analytics(analytics_data_1["data"])
    AnalyticsHelpers.create_analytics(analytics_data_2["data"])
    recent_analytics = AnalyticsHelpers.get_recent_analytics(limit=1)
    assert len(recent_analytics) == 1  # Ensure we get only one recent analytics entry

# Test for deleting analytics
def test_delete_analytics(init_db):
    analytics_data = {
        "data": {"key": "value"}
    }
    analytics = AnalyticsHelpers.create_analytics(analytics_data["data"])
    AnalyticsHelpers.delete_analytics(analytics.id)
    deleted_analytics = Analytics.query.get(analytics.id)
    assert deleted_analytics is None  # Ensure the analytics entry is deleted

# Test for counting the total number of analytics entries
def test_count_analytics(init_db):
    analytics_data_1 = {
        "data": {"key": "value1"}
    }
    analytics_data_2 = {
        "data": {"key": "value2"}
    }
    AnalyticsHelpers.create_analytics(analytics_data_1["data"])
    AnalyticsHelpers.create_analytics(analytics_data_2["data"])
    analytics_count = AnalyticsHelpers.count()
    assert analytics_count == 2  # Ensure the analytics count is correct

# Test for checking if an analytics entry exists
def test_exists_analytics(init_db):
    analytics_data = {
        "data": {"key": "value"}
    }
    analytics = AnalyticsHelpers.create_analytics(analytics_data["data"])
    analytics_exists = AnalyticsHelpers.exists(analytics.id)
    assert analytics_exists is True  # Ensure the analytics entry exists

