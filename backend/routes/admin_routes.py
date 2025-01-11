from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User, Log, db
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import (
    handle_general_error, handle_http_error
)

# Initialize logger
logger = CentralizedLogger("admin_routes")

# Create the admin blueprint
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    """Fetch a list of all users."""
    try:
        admin_user = get_jwt_identity()
        logger.log_to_console("INFO", "Admin user requested user list", user_id=admin_user)

        users = User.query.all()
        user_list = [{"id": user.id, "username": user.username, "email": user.email, "role": user.role} for user in users]

        logger.log_to_console("INFO", "Successfully fetched user list", count=len(user_list))
        return jsonify(user_list), 200
    except Exception as e:
        logger.log_to_console("ERROR", "Error fetching user list", error=str(e))
        return handle_general_error(e)


@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    """Delete a specific user by ID."""
    try:
        admin_user = get_jwt_identity()
        logger.log_to_console("INFO", "Admin user requested user deletion", user_id=admin_user, target_user=user_id)

        user = db.session.get(User, user_id)  # Use Session.get() instead of Query.get()
        if not user:
            logger.log_to_console("WARNING", "User not found for deletion", target_user=user_id)
            return handle_http_error(404, "USER_NOT_FOUND", "User not found.")

        db.session.delete(user)
        db.session.commit()

        logger.log_to_console("INFO", "User deleted successfully", target_user=user_id)
        return jsonify({"message": "User deleted successfully."}), 200
    except Exception as e:
        logger.log_to_console("ERROR", "Error deleting user", error=str(e))
        return handle_general_error(e)


@admin_bp.route("/logs", methods=["GET"])
@jwt_required()
def fetch_logs():
    """Fetch system logs."""
    try:
        admin_user = get_jwt_identity()
        logger.log_to_console("INFO", "Admin user requested logs", user_id=admin_user)

        # Fetch logs sorted by timestamp in descending order
        logs = Log.query.order_by(Log.timestamp.desc()).limit(50).all()
        log_list = [{"action": log.action, "level": log.level, "timestamp": log.timestamp, "meta_data": log.meta_data} for log in logs]

        logger.log_to_console("INFO", "Successfully fetched logs", count=len(log_list))
        return jsonify(log_list), 200
    except Exception as e:
        logger.log_to_console("ERROR", "Error fetching logs", error=str(e))
        return handle_general_error(e)

