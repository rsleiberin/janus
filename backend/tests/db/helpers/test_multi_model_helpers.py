# test_multi_model_helpers.py

import pytest
import logging

from backend.db import db
from backend.db.helpers.log_helpers import LogHelpers
from backend.db.helpers.security_helpers import SecurityHelpers
from backend.db.helpers.user_helpers import UserHelpers
from backend.db.helpers.admin_helpers import AdminHelpers
from backend.db.helpers.analytics_helpers import AnalyticsHelpers
from backend.db.helpers.image_helpers import ImageHelpers

from backend.db.helpers.multi_model_helpers import (
    get_logs_by_user,
    count_user_actions,
    is_user_admin,
    get_admin_level,
    get_analytics_data_for_image,
    track_user_security_actions,
    get_images_with_analytics
)

from backend.models import Security, User, Admin, Log

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("test_logger")



#
# Combined Helper for User and Log Helpers
#

@pytest.mark.usefixtures("function_db_setup")
def test_get_logs_by_user():
    logger.debug("Starting test_get_logs_by_user...")
    user_id = 1
    action = "file_uploaded"
    LogHelpers.create_log(action, user_id)
    logs = get_logs_by_user(user_id)
    assert len(logs) > 0, "Expected logs for the user but got none."
    logger.debug("test_get_logs_by_user passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_count_user_actions():
    logger.debug("Starting test_count_user_actions...")
    user_id = 1
    LogHelpers.create_log("file_uploaded", user_id)
    LogHelpers.create_log("file_deleted", user_id)
    user_action_count = count_user_actions(user_id)
    assert user_action_count == 2, "Expected 2 user actions."
    logger.debug("test_count_user_actions passed successfully.")


#
# Combined Helper for User and Admin Helpers
#

@pytest.mark.usefixtures("function_db_setup")
def test_is_user_admin():
    logger.debug("Starting test_is_user_admin...")
    # Pass a username so it doesn't violate NOT NULL
    user = UserHelpers.create({
        "username": "admin_user", 
        "email": "admin@example.com", 
        "password_hash": "password", 
        "role": "user"
    })

    admin_data = {"user_id": user.id, "admin_level": "superadmin"}
    AdminHelpers.create(admin_data)
    is_admin_result = is_user_admin(user.id)
    assert is_admin_result is True, "Expected user to be recognized as admin."
    logger.debug("test_is_user_admin passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_admin_level():
    logger.debug("Starting test_get_admin_level...")
    # Pass a username so it doesn't violate NOT NULL
    user = UserHelpers.create({
        "username": "admin_user2", 
        "email": "admin2@example.com", 
        "password_hash": "password", 
        "role": "user"
    })

    admin_data = {"user_id": user.id, "admin_level": "superadmin"}
    AdminHelpers.create(admin_data)
    admin_level = get_admin_level(user.id)
    assert admin_level == "superadmin", "Admin level mismatch."
    logger.debug("test_get_admin_level passed successfully.")
#
# Combined Helper for Analytics and Image Helpers
#

@pytest.mark.usefixtures("function_db_setup")
def test_get_analytics_data_for_image():
    logger.debug("Starting test_get_analytics_data_for_image...")
    image = ImageHelpers.create({"filename": "test.jpg", "width": 800, "height": 600})
    analytics_data = {"data": {"key": "value"}}
    AnalyticsHelpers.create_analytics(analytics_data["data"])
    analytics = get_analytics_data_for_image(image.id)
    assert len(analytics) > 0, "Expected analytics data associated with the image."
    logger.debug("test_get_analytics_data_for_image passed successfully.")


#
# Combined Helper for User and Security Helpers
#

@pytest.mark.usefixtures("function_db_setup")
def test_track_user_security_actions():
    logger.debug("Starting test_track_user_security_actions...")
    user_id = 1
    action = "login_attempt"
    SecurityHelpers.create_security_entry(user_id, action)
    security_actions = track_user_security_actions(user_id)
    assert len(security_actions) > 0, "Expected security actions for the user."
    logger.debug("test_track_user_security_actions passed successfully.")


#
# Combined Helper for Image and Analytics Helpers
#

@pytest.mark.usefixtures("function_db_setup")
def test_get_images_with_analytics():
    logger.debug("Starting test_get_images_with_analytics...")
    image_data = {"filename": "test.jpg", "width": 800, "height": 600}
    ImageHelpers.create(image_data)
    analytics_data = {"data": {"key": "value"}}
    AnalyticsHelpers.create_analytics(analytics_data["data"])
    images_with_analytics = get_images_with_analytics()
    assert len(images_with_analytics) > 0, "Expected at least one image with analytics data."
    logger.debug("test_get_images_with_analytics passed successfully.")
