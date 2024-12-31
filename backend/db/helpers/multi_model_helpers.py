# multi_model_helpers.py
from backend.models import Image, User, Admin, Log, Analytics, Security
from backend.db import db
from datetime import datetime

# Combined Helper for User and Log Related Helpers
def get_logs_by_user(user_id):
    """Fetch all logs associated with a user."""
    return Log.query.filter_by(user_id=user_id).all()

def count_user_actions(user_id):
    """Count the number of actions performed by a user."""
    return Log.query.filter_by(user_id=user_id).count()

# Combined Helper for User and Admin Related Helpers
def is_user_admin(user_id):
    """Check if a user has admin privileges."""
    user = User.query.get(user_id)
    if user:
        return Admin.query.filter_by(user_id=user.id).first() is not None
    return False

def get_admin_level(user_id):
    """Fetch the admin level of a user."""
    admin = Admin.query.filter_by(user_id=user_id).first()
    if admin:
        return admin.admin_level
    return None

# Combined Helper for Analytics and Image Related Helpers
def get_analytics_data_for_image(image_id):
    """Fetch analytics data associated with a specific image."""
    image = Image.query.get(image_id)
    if image:
        return Analytics.query.filter_by(id=image_id).all()
    return []

# Combined Helper for User and Security Related Helpers
def track_user_security_actions(user_id):
    """Fetch all security-related actions for a specific user."""
    return Security.query.filter_by(user_id=user_id).all()

# Combined Helper for Image and Analytics Related Helpers
def get_images_with_analytics():
    """Fetch all images with associated analytics data."""
    images = Image.query.all()
    result = []
    for image in images:
        analytics = Analytics.query.filter_by(id=image.id).all()
        result.append({"image": image, "analytics": analytics})
    return result
# Security Model Helpers Tests

# Test for creating a security entry
def test_create_security_entry(init_db):
    user_id = 1
    action = "login_attempt"
    security_entry = SecurityHelpers.create_security_entry(user_id, action)
    assert security_entry.id is not None  # Ensure the security entry has been created with an ID
    assert security_entry.action == action  # Ensure the action is correct
    assert security_entry.user_id == user_id  # Ensure the user_id is correct

# Test for retrieving a security entry by ID
def test_get_security_by_id(init_db):
    user_id = 1
    action = "login_attempt"
    security_entry = SecurityHelpers.create_security_entry(user_id, action)
    fetched_security = SecurityHelpers.get_security_by_id(security_entry.id)
    assert fetched_security.id == security_entry.id  # Ensure the correct security entry is fetched

# Test for retrieving all security entries by user ID
def test_get_security_by_user(init_db):
    user_id = 1
    action = "login_attempt"
    SecurityHelpers.create_security_entry(user_id, action)
    security_entries = SecurityHelpers.get_security_by_user(user_id)
    assert len(security_entries) > 0  # Ensure we get security entries for the user

# Test for retrieving recent security entries
def test_get_recent_security_entries(init_db):
    user_id = 1
    action_1 = "login_attempt"
    action_2 = "password_change"
    SecurityHelpers.create_security_entry(user_id, action_1)
    SecurityHelpers.create_security_entry(user_id, action_2)
    recent_entries = SecurityHelpers.get_recent_security_entries(limit=1)
    assert len(recent_entries) == 1  # Ensure we get only the most recent security entry

# Test for deleting a security entry
def test_delete_security_entry(init_db):
    user_id = 1
    action = "login_attempt"
    security_entry = SecurityHelpers.create_security_entry(user_id, action)
    SecurityHelpers.delete_security_entry(security_entry.id)
    deleted_security = Security.query.get(security_entry.id)
    assert deleted_security is None  # Ensure the security entry has been deleted

# Test for counting the total number of security entries
def test_count_security_entries(init_db):
    user_id = 1
    action = "login_attempt"
    SecurityHelpers.create_security_entry(user_id, action)
    security_count = SecurityHelpers.count()
    assert security_count == 1  # Ensure the count is correct

# Test for checking if a security entry exists
def test_exists_security_entry(init_db):
    user_id = 1
    action = "login_attempt"
    security_entry = SecurityHelpers.create_security_entry(user_id, action)
    security_exists = SecurityHelpers.exists(security_entry.id)
    assert security_exists is True  # Ensure the security entry exists


# Combined Helper for User and Log Related Helpers

# Test for fetching logs by user
def test_get_logs_by_user(init_db):
    user_id = 1
    action = "file_uploaded"
    log = LogHelpers.create_log(action, user_id)
    logs = get_logs_by_user(user_id)
    assert len(logs) > 0  # Ensure we get logs for the user

# Test for counting user actions
def test_count_user_actions(init_db):
    user_id = 1
    action_1 = "file_uploaded"
    action_2 = "file_deleted"
    LogHelpers.create_log(action_1, user_id)
    LogHelpers.create_log(action_2, user_id)
    user_action_count = count_user_actions(user_id)
    assert user_action_count == 2  # Ensure the count of actions is correct


# Combined Helper for User and Admin Related Helpers

# Test for checking if a user is an admin
def test_is_user_admin(init_db):
    user_id = 1
    user = UserHelpers.create({"email": "admin@example.com", "password": "password", "role": "user"})
    admin_data = {"user_id": user.id, "admin_level": "superadmin"}
    AdminHelpers.create(admin_data)
    is_admin = is_user_admin(user.id)
    assert is_admin is True  # Ensure the user has admin privileges

# Test for fetching the admin level
def test_get_admin_level(init_db):
    user_id = 1
    user = UserHelpers.create({"email": "admin@example.com", "password": "password", "role": "user"})
    admin_data = {"user_id": user.id, "admin_level": "superadmin"}
    AdminHelpers.create(admin_data)
    admin_level = get_admin_level(user.id)
    assert admin_level == "superadmin"  # Ensure the correct admin level is fetched


# Combined Helper for Analytics and Image Related Helpers

# Test for fetching analytics data for a specific image
def test_get_analytics_data_for_image(init_db):
    image_data = {"filename": "test.jpg", "width": 800, "height": 600}
    image = ImageHelpers.create(image_data)
    analytics_data = {"data": {"key": "value"}}
    AnalyticsHelpers.create_analytics(analytics_data["data"])
    analytics = get_analytics_data_for_image(image.id)
    assert len(analytics) > 0  # Ensure we get analytics data associated with the image


# Combined Helper for User and Security Related Helpers

# Test for fetching all security actions for a user
def test_track_user_security_actions(init_db):
    user_id = 1
    action = "login_attempt"
    SecurityHelpers.create_security_entry(user_id, action)
    security_actions = track_user_security_actions(user_id)
    assert len(security_actions) > 0  # Ensure we get security actions for the user


# Combined Helper for Image and Analytics Related Helpers

# Test for fetching all images with associated analytics data
def test_get_images_with_analytics(init_db):
    image_data = {"filename": "test.jpg", "width": 800, "height": 600}
    image = ImageHelpers.create(image_data)
    analytics_data = {"data": {"key": "value"}}
    AnalyticsHelpers.create_analytics(analytics_data["data"])
    images_with_analytics = get_images_with_analytics()
    assert len(images_with_analytics) > 0  # Ensure we get images with analytics data

