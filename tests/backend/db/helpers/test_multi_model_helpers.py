import pytest
from datetime import datetime
from sqlalchemy.sql import text
from backend.db import db
from backend.utils.logger import CentralizedLogger
from backend.db.helpers.multi_model_helpers import (
    get_logs_by_user,
    count_user_actions,
    is_user_admin,
    get_admin_level,
    get_analytics_data_for_image,
    track_user_security_actions,
    get_images_with_analytics,
)

logger = CentralizedLogger("test_multi_model_helpers")


@pytest.mark.usefixtures("function_db_setup")
def test_get_logs_by_user():
    logger.log_to_console("DEBUG", "Starting test_get_logs_by_user...")
    insert_query = text(
        """
        INSERT INTO logs (action, user_id, log_metadata, level, timestamp, module)
        VALUES
        ('Action 1', 1, '{"key": "value"}', 'INFO', :timestamp, NULL),
        ('Action 2', 1, '{"key": "value2"}', 'INFO', :timestamp, NULL)
        """
    )
    db.session.execute(insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    logs = get_logs_by_user(1)
    assert len(logs) == 2, f"Expected 2 logs, found {len(logs)}."


@pytest.mark.usefixtures("function_db_setup")
def test_count_user_actions():
    logger.log_to_console("DEBUG", "Starting test_count_user_actions...")
    insert_query = text(
        """
        INSERT INTO logs (action, user_id, log_metadata, level, timestamp, module)
        VALUES
        ('Action 1', 1, '{"key": "value"}', 'INFO', :timestamp, NULL),
        ('Action 2', 1, '{"key": "value2"}', 'INFO', :timestamp, NULL)
        """
    )
    db.session.execute(insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    count = count_user_actions(1)
    assert count == 2, f"Expected 2 actions, found {count}."


@pytest.mark.usefixtures("function_db_setup")
def test_is_user_admin():
    logger.log_to_console("DEBUG", "Starting test_is_user_admin...")
    user_insert_query = text(
        """
        INSERT INTO users (username, email, password_hash)
        VALUES ('admin_user', 'admin@example.com', 'hashed_password')
        """
    )
    db.session.execute(user_insert_query)
    db.session.commit()

    admin_insert_query = text(
        """
        INSERT INTO admins (user_id, admin_level)
        VALUES (1, 'superadmin')
        """
    )
    db.session.execute(admin_insert_query)
    db.session.commit()

    is_admin_flag = is_user_admin(1)
    assert is_admin_flag, "Expected user to be an admin."


@pytest.mark.usefixtures("function_db_setup")
def test_get_admin_level():
    logger.log_to_console("DEBUG", "Starting test_get_admin_level...")
    user_insert_query = text(
        """
        INSERT INTO users (username, email, password_hash)
        VALUES ('admin_user', 'admin@example.com', 'hashed_password')
        """
    )
    db.session.execute(user_insert_query)
    db.session.commit()

    admin_insert_query = text(
        """
        INSERT INTO admins (user_id, admin_level)
        VALUES (1, 'superadmin')
        """
    )
    db.session.execute(admin_insert_query)
    db.session.commit()

    admin_level = get_admin_level(1)
    assert admin_level == "superadmin", f"Expected 'superadmin', got {admin_level}."


@pytest.mark.usefixtures("function_db_setup")
def test_get_analytics_data_for_image():
    logger.log_to_console("DEBUG", "Starting test_get_analytics_data_for_image...")
    analytics_insert_query = text(
        """
        INSERT INTO analytics (data, research_topic, created_at)
        VALUES ('{"metric": "value"}', 'test_topic', :timestamp)
        """
    )
    db.session.execute(analytics_insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    analytics_data = get_analytics_data_for_image(1)
    assert (
        len(analytics_data) == 1
    ), f"Expected 1 analytics entry, found {len(analytics_data)}."


@pytest.mark.usefixtures("function_db_setup")
def test_track_user_security_actions():
    logger.log_to_console("DEBUG", "Starting test_track_user_security_actions...")
    security_insert_query = text(
        """
        INSERT INTO security (user_id, action, timestamp)
        VALUES
        (1, 'Login Attempt', :timestamp),
        (1, 'Password Change', :timestamp)
        """
    )
    db.session.execute(security_insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    actions = track_user_security_actions(1)
    assert len(actions) == 2, f"Expected 2 actions, found {len(actions)}."


@pytest.mark.usefixtures("function_db_setup")
def test_get_images_with_analytics():
    logger.log_to_console("DEBUG", "Starting test_get_images_with_analytics...")

    user_insert_query = text(
        """
        INSERT INTO users (username, email, password_hash)
        VALUES ('sample_user', 'user@example.com', 'hashed_password')
        """
    )
    db.session.execute(user_insert_query)
    db.session.commit()

    image_insert_query = text(
        """
        INSERT INTO images (user_id, filename, width, height, created_at, updated_at)
        VALUES (1, 'test_image.png', 1920, 1080, :timestamp, :timestamp)
        """
    )
    db.session.execute(image_insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    analytics_insert_query = text(
        """
        INSERT INTO analytics (data, research_topic, created_at)
        VALUES ('{"metric": "value"}', 'test_topic', :timestamp)
        """
    )
    db.session.execute(analytics_insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    images_with_analytics = get_images_with_analytics()
    assert (
        len(images_with_analytics) == 1
    ), f"Expected 1 image with analytics, found {len(images_with_analytics)}."
    assert isinstance(
        images_with_analytics[0]["analytics"], list
    ), "Analytics should be a list."
    assert (
        len(images_with_analytics[0]["analytics"]) == 1
    ), "Expected 1 analytics entry for the image."
