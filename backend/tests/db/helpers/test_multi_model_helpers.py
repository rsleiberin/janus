import pytest
from datetime import datetime
from sqlalchemy.sql import text
from backend.db import db
from backend.models import Image, User, Admin, Log, Analytics, Security
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
from backend.utils.error_handling.db.errors import (
    LogsByUserError,
    UserActionCountError,
    AdminCheckError,
    AdminLevelFetchError,
    AnalyticsForImageError,
    SecurityActionsFetchError,
    ImagesWithAnalyticsError,
)

logger = CentralizedLogger("test_multi_model_helpers")

@pytest.mark.usefixtures("function_db_setup")
def test_get_logs_by_user():
    logger.log_to_console("DEBUG", "Starting test_get_logs_by_user...")
    insert_query = text("""
        INSERT INTO logs (action, user_id, meta_data, level, timestamp, module)
        VALUES
        ('Action 1', 1, '{"key": "value"}', 'INFO', :timestamp, NULL),
        ('Action 2', 1, '{"key": "value2"}', 'INFO', :timestamp, NULL)
    """)
    db.session.execute(insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    try:
        logs = get_logs_by_user(1)
        assert len(logs) == 2, f"Expected 2 logs, found {len(logs)}."
    except LogsByUserError as e:
        pytest.fail(str(e))


@pytest.mark.usefixtures("function_db_setup")
def test_count_user_actions():
    logger.log_to_console("DEBUG", "Starting test_count_user_actions...")
    insert_query = text("""
        INSERT INTO logs (action, user_id, meta_data, level, timestamp, module)
        VALUES
        ('Action 1', 1, '{"key": "value"}', 'INFO', :timestamp, NULL),
        ('Action 2', 1, '{"key": "value2"}', 'INFO', :timestamp, NULL)
    """)
    db.session.execute(insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    try:
        count = count_user_actions(1)
        assert count == 2, f"Expected 2 actions, found {count}."
    except UserActionCountError as e:
        pytest.fail(str(e))


@pytest.mark.usefixtures("function_db_setup")
def test_is_user_admin():
    logger.log_to_console("DEBUG", "Starting test_is_user_admin...")
    user_insert_query = text("""
        INSERT INTO users (username, email, password_hash, role)
        VALUES ('admin_user', 'admin@example.com', 'hashed_password', 'admin')
    """)
    db.session.execute(user_insert_query)
    db.session.commit()

    admin_insert_query = text("""
        INSERT INTO admins (user_id, admin_level)
        VALUES (1, 'superadmin')
    """)
    db.session.execute(admin_insert_query)
    db.session.commit()

    try:
        is_admin = is_user_admin(1)
        assert is_admin, "Expected user to be an admin."
    except AdminCheckError as e:
        pytest.fail(str(e))


@pytest.mark.usefixtures("function_db_setup")
def test_get_admin_level():
    logger.log_to_console("DEBUG", "Starting test_get_admin_level...")
    user_insert_query = text("""
        INSERT INTO users (username, email, password_hash, role)
        VALUES ('admin_user', 'admin@example.com', 'hashed_password', 'admin')
    """)
    db.session.execute(user_insert_query)
    db.session.commit()

    admin_insert_query = text("""
        INSERT INTO admins (user_id, admin_level)
        VALUES (1, 'superadmin')
    """)
    db.session.execute(admin_insert_query)
    db.session.commit()

    try:
        admin_level = get_admin_level(1)
        assert admin_level == 'superadmin', f"Expected 'superadmin', got {admin_level}."
    except AdminLevelFetchError as e:
        pytest.fail(str(e))


@pytest.mark.usefixtures("function_db_setup")
def test_get_analytics_data_for_image():
    logger.log_to_console("DEBUG", "Starting test_get_analytics_data_for_image...")
    analytics_insert_query = text("""
        INSERT INTO analytics (data, research_topic, created_at)
        VALUES ('{"metric": "value"}', 'test_topic', :timestamp)
    """)
    db.session.execute(analytics_insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    try:
        analytics_data = get_analytics_data_for_image(1)
        assert len(analytics_data) == 1, f"Expected 1 analytics entry, found {len(analytics_data)}."
    except AnalyticsForImageError as e:
        pytest.fail(str(e))


@pytest.mark.usefixtures("function_db_setup")
def test_track_user_security_actions():
    logger.log_to_console("DEBUG", "Starting test_track_user_security_actions...")
    security_insert_query = text("""
        INSERT INTO security (user_id, action, timestamp)
        VALUES
        (1, 'Login Attempt', :timestamp),
        (1, 'Password Change', :timestamp)
    """)
    db.session.execute(security_insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    try:
        actions = track_user_security_actions(1)
        assert len(actions) == 2, f"Expected 2 actions, found {len(actions)}."
    except SecurityActionsFetchError as e:
        pytest.fail(str(e))


@pytest.mark.usefixtures("function_db_setup")
def test_get_images_with_analytics():
    logger.log_to_console("DEBUG", "Starting test_get_images_with_analytics...")
    image_insert_query = text("""
        INSERT INTO images (filename, width, height, created_at, updated_at)
        VALUES ('test_image.png', 1920, 1080, :timestamp, :timestamp)
    """)
    db.session.execute(image_insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    analytics_insert_query = text("""
        INSERT INTO analytics (data, research_topic, created_at)
        VALUES ('{"metric": "value"}', 'test_topic', :timestamp)
    """)
    db.session.execute(analytics_insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    try:
        images_with_analytics = get_images_with_analytics()
        assert len(images_with_analytics) == 1, f"Expected 1 image with analytics, found {len(images_with_analytics)}."
        assert len(images_with_analytics[0]['analytics']) == 1, "Expected 1 analytics entry for the image."
    except ImagesWithAnalyticsError as e:
        pytest.fail(str(e))
