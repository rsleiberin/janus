"""
Admin routes for managing users and logs.
"""

# pylint: disable=broad-exception-caught,R1710

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.db import db
from backend.models import User, Admin, Log
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
    A before_request hook ensuring the current user is an admin.
    """
    current_user = get_jwt_identity()
    admin_record = db.session.query(Admin).filter_by(user_id=current_user["id"]).first()
    if not admin_record:
        logger.log_to_console(
            "WARNING",
            "Non-admin user tried to access admin route.",
            user_id=current_user["id"],
        )
        return jsonify({"error": "Admin privileges required."}), 403


@admin_bp.route("/users", methods=["GET"])
def list_users():
    """
    Fetch a list of all users (admin only).
    """
    try:
        users = User.query.all()
        user_list = []
        for user in users:
            user_list.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            )

        logger.log_to_console("INFO", "Admin fetched user list.", count=len(user_list))
        return jsonify(user_list), 200
    except Exception as exc:
        logger.log_to_console("ERROR", "Error fetching user list.", error=str(exc))
        return handle_general_error(exc)


@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete a specific user by ID (admin only).
    """
    try:
        user = db.session.get(User, user_id)
        if not user:
            logger.log_to_console("WARNING", "User not found.", user_id=user_id)
            return handle_http_error(404, "USER_NOT_FOUND", "User not found.")

        db.session.delete(user)
        db.session.commit()

        logger.log_to_console("INFO", "User deleted successfully.", target_user=user_id)
        return jsonify({"message": "User deleted successfully."}), 200
    except Exception as exc:
        logger.log_to_console("ERROR", "Error deleting user.", error=str(exc))
        return handle_general_error(exc)


@admin_bp.route("/logs", methods=["GET"])
def fetch_logs():
    """
    Fetch system logs in descending order by timestamp (admin only).
    """
    try:
        logs = Log.query.order_by(Log.timestamp.desc()).all()
        log_list = []
        for log_entry in logs:
            log_list.append(
                {
                    "id": log_entry.id,
                    "action": log_entry.action,
                    "user_id": log_entry.user_id,
                    "timestamp": (
                        log_entry.timestamp.isoformat() if log_entry.timestamp else None
                    ),
                    "module": log_entry.module,
                    "level": log_entry.level,
                    "log_metadata": log_entry.log_metadata,
                }
            )

        logger.log_to_console("INFO", "Fetched logs.", count=len(log_list))
        return jsonify(log_list), 200
    except Exception as exc:
        logger.log_to_console("ERROR", "Error fetching logs.", error=str(exc))
        return handle_general_error(exc)
