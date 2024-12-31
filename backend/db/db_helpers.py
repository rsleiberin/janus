# Importing necessary modules
from backend.db import db
from backend.models import Image, User, Admin, Log, Analytics, Security
from datetime import datetime

# Image Model Helpers
class ImageHelpers:
    
    @staticmethod
    def create(image_data):
        """Create a new image record."""
        image = Image(**image_data)
        db.session.add(image)
        db.session.commit()
        return image

    @staticmethod
    def get_by_id(image_id):
        """Get an image by its ID."""
        return Image.query.get(image_id)

    @staticmethod
    def update(image_id, updated_data):
        """Update an existing image record."""
        image = Image.query.get(image_id)
        if image:
            for key, value in updated_data.items():
                setattr(image, key, value)
            db.session.commit()
        return image

    @staticmethod
    def delete(image_id):
        """Delete an image by its ID."""
        image = Image.query.get(image_id)
        if image:
            db.session.delete(image)
            db.session.commit()

    @staticmethod
    def get_all():
        """Get all images."""
        return Image.query.all()

    @staticmethod
    def filter_by(field, value):
        """Filter images by a specific field."""
        return Image.query.filter(getattr(Image, field) == value).all()

    @staticmethod
    def count():
        """Get the number of images."""
        return Image.query.count()

    @staticmethod
    def exists(image_id):
        """Check if an image with a specific ID exists."""
        return Image.query.filter_by(id=image_id).first() is not None

    @staticmethod
    def get_by_filename(filename):
        """Get an image by its filename."""
        return Image.query.filter_by(filename=filename).first()

    @staticmethod
    def get_images_by_date_range(start_date, end_date):
        """Get images created within a specific date range."""
        return Image.query.filter(
            Image.created_at >= start_date, Image.created_at <= end_date
        ).all()

    @staticmethod
    def get_images_by_size(min_width, min_height):
        """Get images larger than a specified size."""
        return Image.query.filter(
            Image.width >= min_width, Image.height >= min_height
        ).all()

    @staticmethod
    def get_by_metadata(metadata):
        """Get images by specific metadata."""
        return Image.query.filter_by(image_metadata=metadata).all()

# User Model Helpers
class UserHelpers:

    @staticmethod
    def create(user_data):
        """Create a new user record."""
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_id(user_id):
        """Get a user by their ID."""
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        """Get a user by their email."""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def update(user_id, updated_data):
        """Update an existing user record."""
        user = User.query.get(user_id)
        if user:
            for key, value in updated_data.items():
                setattr(user, key, value)
            db.session.commit()
        return user

    @staticmethod
    def delete(user_id):
        """Delete a user by their ID."""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    @staticmethod
    def count():
        """Get the number of users."""
        return User.query.count()

    @staticmethod
    def exists(user_id):
        """Check if a user with a specific ID exists."""
        return User.query.filter_by(id=user_id).first() is not None
# Admin Model Helpers
class AdminHelpers:

    @staticmethod
    def create(admin_data):
        """Create a new admin record, linking it to a user."""
        admin = Admin(**admin_data)
        db.session.add(admin)
        db.session.commit()
        return admin

    @staticmethod
    def get_by_id(admin_id):
        """Get an admin by their ID."""
        return Admin.query.get(admin_id)

    @staticmethod
    def get_by_user_id(user_id):
        """Get an admin by the associated user's ID."""
        return Admin.query.filter_by(user_id=user_id).first()

    @staticmethod
    def update(admin_id, updated_data):
        """Update an existing admin record."""
        admin = Admin.query.get(admin_id)
        if admin:
            for key, value in updated_data.items():
                setattr(admin, key, value)
            db.session.commit()
        return admin

    @staticmethod
    def delete(admin_id):
        """Delete an admin by their ID."""
        admin = Admin.query.get(admin_id)
        if admin:
            db.session.delete(admin)
            db.session.commit()

    @staticmethod
    def count():
        """Get the number of admins."""
        return Admin.query.count()

    @staticmethod
    def exists(admin_id):
        """Check if an admin with a specific ID exists."""
        return Admin.query.filter_by(id=admin_id).first() is not None
# Log Model Helpers
class LogHelpers:

    @staticmethod
    def create_log(action, user_id):
        """Create a new log entry for a user action."""
        log = Log(action=action, user_id=user_id)
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def get_by_id(log_id):
        """Get a log by its ID."""
        return Log.query.get(log_id)

    @staticmethod
    def get_by_user_id(user_id):
        """Get logs by the user ID."""
        return Log.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_recent_logs(limit=10):
        """Get the most recent logs."""
        return Log.query.order_by(Log.timestamp.desc()).limit(limit).all()

    @staticmethod
    def delete_log(log_id):
        """Delete a log entry by its ID."""
        log = Log.query.get(log_id)
        if log:
            db.session.delete(log)
            db.session.commit()

    @staticmethod
    def count():
        """Get the total number of logs."""
        return Log.query.count()

    @staticmethod
    def exists(log_id):
        """Check if a log entry exists."""
        return Log.query.filter_by(id=log_id).first() is not None

# Analytics Model Helpers
class AnalyticsHelpers:

    @staticmethod
    def create_analytics(data):
        """Create new analytics entry with the provided data."""
        analytics = Analytics(data=data)
        db.session.add(analytics)
        db.session.commit()
        return analytics

    @staticmethod
    def get_by_id(analytics_id):
        """Get analytics by its ID."""
        return Analytics.query.get(analytics_id)

    @staticmethod
    def get_all_analytics():
        """Get all analytics entries."""
        return Analytics.query.all()

    @staticmethod
    def get_recent_analytics(limit=10):
        """Get the most recent analytics entries."""
        return Analytics.query.order_by(Analytics.created_at.desc()).limit(limit).all()

    @staticmethod
    def delete_analytics(analytics_id):
        """Delete an analytics entry by its ID."""
        analytics = Analytics.query.get(analytics_id)
        if analytics:
            db.session.delete(analytics)
            db.session.commit()

    @staticmethod
    def count():
        """Get the total number of analytics entries."""
        return Analytics.query.count()

    @staticmethod
    def exists(analytics_id):
        """Check if an analytics entry exists."""
        return Analytics.query.filter_by(id=analytics_id).first() is not None
# Security Model Helpers
class SecurityHelpers:

    @staticmethod
    def create_security_entry(user_id, action):
        """Create a new security entry for a user."""
        security_entry = Security(user_id=user_id, action=action)
        db.session.add(security_entry)
        db.session.commit()
        return security_entry

    @staticmethod
    def get_security_by_id(security_id):
        """Get a security entry by its ID."""
        return Security.query.get(security_id)

    @staticmethod
    def get_security_by_user(user_id):
        """Get all security entries for a specific user."""
        return Security.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_recent_security_entries(limit=10):
        """Get the most recent security entries."""
        return Security.query.order_by(Security.timestamp.desc()).limit(limit).all()

    @staticmethod
    def delete_security_entry(security_id):
        """Delete a security entry by its ID."""
        security_entry = Security.query.get(security_id)
        if security_entry:
            db.session.delete(security_entry)
            db.session.commit()

    @staticmethod
    def count():
        """Get the total number of security entries."""
        return Security.query.count()

    @staticmethod
    def exists(security_id):
        """Check if a security entry exists."""
        return Security.query.filter_by(id=security_id).first() is not None
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

