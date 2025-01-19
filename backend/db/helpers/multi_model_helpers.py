from backend.db import db
from backend.models import (
    Image,
    Admin,
    Log,
    Analytics,
    Security,
)
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.db.errors import (
    LogsByUserError,
    UserActionCountError,
    AdminCheckError,
    AdminLevelFetchError,
    AnalyticsForImageError,
    SecurityActionsFetchError,
    ImagesWithAnalyticsError,
    handle_database_error,
)

logger = CentralizedLogger("multi_model_helpers")


def get_logs_by_user(user_id):
    """Fetch all logs associated with a user."""
    try:
        logs = db.session.query(Log).filter_by(user_id=user_id).all()
        logger.log_to_console(
            "DEBUG", "Fetched logs by user", user_id=user_id, count=len(logs)
        )
        return logs
    except Exception as e:
        error = LogsByUserError(f"Failed to fetch logs for user ID {user_id}: {str(e)}")
        logger.log_to_console("ERROR", str(error), user_id=user_id)
        raise handle_database_error(
            error, module="multi_model_helpers", meta_data={"user_id": user_id}
        )


def count_user_actions(user_id):
    """Count the number of actions performed by a user."""
    try:
        count = db.session.query(Log).filter_by(user_id=user_id).count()
        logger.log_to_console(
            "DEBUG", "Counted user actions", user_id=user_id, count=count
        )
        return count
    except Exception as e:
        error = UserActionCountError(
            f"Failed to count actions for user ID {user_id}: {str(e)}"
        )
        logger.log_to_console("ERROR", str(error), user_id=user_id)
        raise handle_database_error(
            error, module="multi_model_helpers", meta_data={"user_id": user_id}
        )


def is_user_admin(user_id):
    """Check if a user has admin privileges."""
    try:
        admin_exists = (
            db.session.query(Admin).filter_by(user_id=user_id).first() is not None
        )
        logger.log_to_console(
            "DEBUG", "Checked admin status", user_id=user_id, is_admin=admin_exists
        )
        return admin_exists
    except Exception as e:
        error = AdminCheckError(
            f"Failed to check admin status for user ID {user_id}: {str(e)}"
        )
        logger.log_to_console("ERROR", str(error), user_id=user_id)
        raise handle_database_error(
            error, module="multi_model_helpers", meta_data={"user_id": user_id}
        )


def get_admin_level(user_id):
    """Fetch the admin level of a user."""
    try:
        admin = db.session.query(Admin).filter_by(user_id=user_id).first()
        admin_level = admin.admin_level if admin else None
        logger.log_to_console(
            "DEBUG", "Fetched admin level", user_id=user_id, admin_level=admin_level
        )
        return admin_level
    except Exception as e:
        error = AdminLevelFetchError(
            f"Failed to fetch admin level for user ID {user_id}: {str(e)}"
        )
        logger.log_to_console("ERROR", str(error), user_id=user_id)
        raise handle_database_error(
            error, module="multi_model_helpers", meta_data={"user_id": user_id}
        )


def get_analytics_data_for_image(image_id):
    """Fetch analytics data associated with a specific image."""
    try:
        analytics_data = db.session.query(Analytics).filter_by(id=image_id).all()
        logger.log_to_console(
            "DEBUG",
            "Fetched analytics data for image",
            image_id=image_id,
            count=len(analytics_data),
        )
        return analytics_data
    except Exception as e:
        error = AnalyticsForImageError(
            f"Failed to fetch analytics data for image ID {image_id}: {str(e)}"
        )
        logger.log_to_console("ERROR", str(error), image_id=image_id)
        raise handle_database_error(
            error, module="multi_model_helpers", meta_data={"image_id": image_id}
        )


def track_user_security_actions(user_id):
    """Fetch all security-related actions for a specific user."""
    try:
        actions = db.session.query(Security).filter_by(user_id=user_id).all()
        logger.log_to_console(
            "DEBUG",
            "Fetched security actions for user",
            user_id=user_id,
            count=len(actions),
        )
        return actions
    except Exception as e:
        error = SecurityActionsFetchError(
            f"Failed to fetch security actions for user ID {user_id}: {str(e)}"
        )
        logger.log_to_console("ERROR", str(error), user_id=user_id)
        raise handle_database_error(
            error, module="multi_model_helpers", meta_data={"user_id": user_id}
        )


def get_images_with_analytics():
    """Fetch all images with associated analytics data."""
    try:
        images = db.session.query(Image).all()
        result = []
        for image in images:
            analytics = db.session.query(Analytics).filter_by(id=image.id).all()
            result.append({"image": image, "analytics": analytics})
        logger.log_to_console(
            "DEBUG", "Fetched images with analytics", count=len(result)
        )
        return result
    except Exception as e:
        error = ImagesWithAnalyticsError(
            f"Failed to fetch images with analytics: {str(e)}"
        )
        logger.log_to_console("ERROR", str(error))
        raise handle_database_error(error, module="multi_model_helpers")
