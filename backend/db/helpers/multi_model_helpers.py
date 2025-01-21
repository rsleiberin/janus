from typing import List, Optional, Dict
from datetime import datetime
from backend.db import db
from backend.models import Image, Admin, Log, Analytics, Security
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.db.errors import handle_database_error

logger = CentralizedLogger("multi_model_helpers")


def get_logs_by_user(user_id: int) -> List[Log]:
    """
    Fetch all logs associated with a user.
    """
    try:
        logs = db.session.query(Log).filter_by(user_id=user_id).all()
        logger.log_to_console("DEBUG", f"Fetched {len(logs)} logs for user ID {user_id}.")
        return logs
    except Exception as e:
        raise handle_database_error(e, module="multi_model_helpers", meta_data={"user_id": user_id})


def count_user_actions(user_id: int) -> int:
    """
    Count the number of actions performed by a user.
    """
    try:
        count = db.session.query(Log).filter_by(user_id=user_id).count()
        logger.log_to_console("DEBUG", f"Counted {count} actions for user ID {user_id}.")
        return count
    except Exception as e:
        raise handle_database_error(e, module="multi_model_helpers", meta_data={"user_id": user_id})


def is_user_admin(user_id: int) -> bool:
    """
    Check if a user has admin privileges.
    """
    try:
        admin_exists = db.session.query(Admin).filter_by(user_id=user_id).first() is not None
        logger.log_to_console("DEBUG", f"User ID {user_id} admin status: {admin_exists}.")
        return admin_exists
    except Exception as e:
        raise handle_database_error(e, module="multi_model_helpers", meta_data={"user_id": user_id})


def get_admin_level(user_id: int) -> Optional[str]:
    """
    Fetch the admin level of a user.
    """
    try:
        admin = db.session.query(Admin).filter_by(user_id=user_id).first()
        admin_level = admin.admin_level if admin else None
        logger.log_to_console("DEBUG", f"Admin level for user ID {user_id}: {admin_level}.")
        return admin_level
    except Exception as e:
        raise handle_database_error(e, module="multi_model_helpers", meta_data={"user_id": user_id})


def get_analytics_data_for_image(image_id: int) -> List[Analytics]:
    """
    Fetch analytics data associated with a specific image.
    """
    try:
        analytics_data = db.session.query(Analytics).filter_by(id=image_id).all()
        logger.log_to_console("DEBUG", f"Fetched {len(analytics_data)} analytics records for image ID {image_id}.")
        return analytics_data
    except Exception as e:
        raise handle_database_error(e, module="multi_model_helpers", meta_data={"image_id": image_id})


def track_user_security_actions(user_id: int) -> List[Security]:
    """
    Fetch all security-related actions for a specific user.
    """
    try:
        actions = db.session.query(Security).filter_by(user_id=user_id).all()
        logger.log_to_console("DEBUG", f"Fetched {len(actions)} security actions for user ID {user_id}.")
        return actions
    except Exception as e:
        raise handle_database_error(e, module="multi_model_helpers", meta_data={"user_id": user_id})


def get_images_with_analytics() -> List[Dict[str, object]]:
    """
    Fetch all images with associated analytics data.
    """
    try:
        images_with_analytics = (
            db.session.query(Image, Analytics)
            .join(Analytics, Image.id == Analytics.id)
            .all()
        )
        result = [
            {"image": image, "analytics": analytics}
            for image, analytics in images_with_analytics
        ]
        logger.log_to_console("DEBUG", f"Fetched {len(result)} images with analytics data.")
        return result
    except Exception as e:
        raise handle_database_error(e, module="multi_model_helpers")
