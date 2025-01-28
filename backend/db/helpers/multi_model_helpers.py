# File: backend/db/helpers/multi_model_helpers.py
# pylint: disable=R1710,W0718

"""
Provides cross-model queries or operations that involve multiple tables.
"""

from typing import List, Optional, Dict
from backend.models import Image, Admin, Log, Analytics, Security
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import handle_database_error

logger = CentralizedLogger("multi_model_helpers")


def get_logs_by_user(user_id: int) -> List[Log]:
    """
    Fetch all logs associated with a user from the Log model.
    """
    try:
        logs = Log.query.filter_by(user_id=user_id).all()
        logger.log_to_console("DEBUG", f"Fetched {len(logs)} logs for user {user_id}.")
        return logs
    except Exception as err:
        handle_database_error(
            err, module="multi_model_helpers", meta_data={"user_id": user_id}
        )


def count_user_actions(user_id: int) -> int:
    """
    Count the number of actions performed by a user (Log entries).
    """
    try:
        total = Log.query.filter_by(user_id=user_id).count()
        logger.log_to_console("DEBUG", f"Counted {total} actions for user {user_id}.")
        return total
    except Exception as err:
        handle_database_error(
            err, module="multi_model_helpers", meta_data={"user_id": user_id}
        )


def is_user_admin(user_id: int) -> bool:
    """
    Check if a user has an Admin record.
    """
    try:
        exists = Admin.query.filter_by(user_id=user_id).first() is not None
        logger.log_to_console("DEBUG", f"User {user_id} admin status: {exists}.")
        return exists
    except Exception as err:
        handle_database_error(
            err, module="multi_model_helpers", meta_data={"user_id": user_id}
        )


def get_admin_level(user_id: int) -> Optional[str]:
    """
    Fetch the admin_level from Admin table if it exists.
    """
    try:
        admin_rec = Admin.query.filter_by(user_id=user_id).first()
        level = admin_rec.admin_level if admin_rec else None
        logger.log_to_console("DEBUG", f"Admin level for user {user_id}: {level}.")
        return level
    except Exception as err:
        handle_database_error(
            err, module="multi_model_helpers", meta_data={"user_id": user_id}
        )


def get_analytics_data_for_image(image_id: int) -> List[Analytics]:
    """
    Example function: fetch Analytics by image ID, if that logic is appropriate.
    Note: currently, Analytics doesn't store an image_id, so this is hypothetical.
    """
    try:
        analytics_data = Analytics.query.filter_by(id=image_id).all()
        logger.log_to_console(
            "DEBUG",
            f"Fetched {len(analytics_data)} analytics records for image ID {image_id}.",
        )
        return analytics_data
    except Exception as err:
        handle_database_error(
            err, module="multi_model_helpers", meta_data={"image_id": image_id}
        )


def track_user_security_actions(user_id: int) -> List[Security]:
    """
    Fetch all security-related actions for a specific user.
    """
    try:
        actions = Security.query.filter_by(user_id=user_id).all()
        logger.log_to_console(
            "DEBUG", f"Fetched {len(actions)} security actions for user {user_id}."
        )
        return actions
    except Exception as err:
        handle_database_error(
            err, module="multi_model_helpers", meta_data={"user_id": user_id}
        )


def get_images_with_analytics() -> List[Dict[str, object]]:
    """
    Example cross-model aggregator: For each Image, fetch related Analytics data.
    In your current schema, there's no direct link between Image & Analytics.
    """
    try:
        images = Image.query.all()
        result = []
        for image in images:
            analytics = Analytics.query.filter(Analytics.id == image.id).all()
            result.append({"image": image, "analytics": analytics})
        logger.log_to_console(
            "DEBUG", f"Fetched {len(result)} images with analytics data."
        )
        return result
    except Exception as err:
        handle_database_error(err, module="multi_model_helpers")
