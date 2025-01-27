"""
Admin routes with a robust role check.
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.db import db
from backend.models import User, Log
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import (
    handle_general_error,
    handle_http_error,
)

logger = CentralizedLogger("admin_routes")
admin_bp = Blueprint("admin", __name__)


@admin_bp.before_request
@jwt_required()
def require_admin():
    """
    A before_request hook ensuring the current user has role='admin'.
    If you store roles in user.role, check it here.
    """
    current_user = get_jwt_identity()
    user_record = db.session.get(User, current_user["id"])
    if not user_record or getattr(user_record, "role", "user") != "admin":
        logger.log_to_console(
            "WARNING",
            "Non-admin user tried to access admin route.",
            user_id=current_user["id"],
        )
        return jsonify({"error": "Admin privileges required."}), 403
    # If admin, explicitly return None so that pylint sees "consistent return"
    return None


@admin_bp.route("/users", methods=["GET"])
def list_users():
    """
    Fetch a list of all users (admin only).
    """
    try:
        current_user = get_jwt_identity()
        logger.log_to_console(
            "INFO", "Admin user requested user list", user_id=current_user
        )

        users = User.query.all()
        user_list = [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "role": getattr(u, "role", "user"),
            }
            for u in users
        ]
        logger.log_to_console(
            "INFO", "Successfully fetched user list", count=len(user_list)
        )
        return jsonify(user_list), 200
    except Exception as exc:  # pylint: disable=W0718
        logger.log_to_console("ERROR", "Error fetching user list", error=str(exc))
        return handle_general_error(exc)


@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete a specific user by ID (admin only).
    """
    try:
        current_user = get_jwt_identity()
        logger.log_to_console(
            "INFO",
            "Admin user requested user deletion",
            user_id=current_user,
            target_user=user_id,
        )

        user = db.session.get(User, user_id)
        if not user:
            logger.log_to_console(
                "WARNING", "User not found for deletion", target_user=user_id
            )
            return handle_http_error(404, "USER_NOT_FOUND", "User not found.")

        db.session.delete(user)
        db.session.commit()

        logger.log_to_console("INFO", "User deleted successfully", target_user=user_id)
        return jsonify({"message": "User deleted successfully."}), 200
    except Exception as exc:  # pylint: disable=W0718
        logger.log_to_console("ERROR", "Error deleting user", error=str(exc))
        return handle_general_error(exc)


@admin_bp.route("/logs", methods=["GET"])
def fetch_logs():
    """
    Fetch system logs in descending order by timestamp (admin only).
    """
    try:
        current_user = get_jwt_identity()
        logger.log_to_console("INFO", "Admin user requested logs", user_id=current_user)

        logs = Log.query.order_by(Log.timestamp.desc()).all()
        log_list = [
            {
                "id": lg.id,
                "action": lg.action,
                "user_id": lg.user_id,
                "timestamp": lg.timestamp.isoformat() if lg.timestamp else None,
                "module": lg.module,
                "level": lg.level,
                "log_metadata": lg.log_metadata,
            }
            for lg in logs
        ]

        logger.log_to_console("INFO", "Successfully fetched logs", count=len(log_list))
        return jsonify(log_list), 200
    except Exception as exc:  # pylint: disable=W0718
        logger.log_to_console("ERROR", "Error fetching logs", error=str(exc))
        return handle_general_error(exc)
