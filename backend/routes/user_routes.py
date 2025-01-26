"""
User routes for profile retrieval and updates.
"""

# pylint: disable=broad-exception-caught

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.db import db
from backend.models import User
from backend.utils.error_handling.error_handling import format_error_response, log_error
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger("user_routes")
user_bp = Blueprint("user", __name__)


@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_user_profile():
    """
    Retrieve the profile of the currently authenticated user.
    """
    try:
        current_user = get_jwt_identity()
        user_obj = db.session.get(User, current_user["id"])
        if not user_obj:
            raise ValueError("User not found.")

        logger.log_to_console(
            "INFO", f"Fetched profile for user ID: {current_user['id']}"
        )
        return (
            jsonify({"username": user_obj.username, "email": user_obj.email}),
            200,
        )

    except ValueError as val_err:
        logger.log_to_console("WARNING", "User not found.", details=str(val_err))
        log_error(
            val_err, module="user_routes", meta_data={"user_id": current_user.get("id")}
        )
        return (
            format_error_response(
                status=404,
                error_code="USER_NOT_FOUND",
                message="The requested user could not be found.",
                details=str(val_err),
            ),
            404,
        )
    except Exception as exc:
        logger.log_to_console(
            "ERROR", "Unexpected error fetching user profile.", exc_info=exc
        )
        log_error(exc, module="user_routes")
        return (
            format_error_response(
                status=500,
                error_code="FETCH_PROFILE_ERROR",
                message="An unexpected error occurred while fetching the user profile.",
                details=str(exc),
            ),
            500,
        )


@user_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_user_profile():
    """
    Update the profile of the currently authenticated user.
    Required JSON: { "username": "NewName" }
    """
    try:
        current_user = get_jwt_identity()
        user_obj = db.session.get(User, current_user["id"])
        if not user_obj:
            raise ValueError("User not found.")

        data = request.json
        if not data or "username" not in data:
            raise ValueError("Invalid user data.")

        user_obj.username = data["username"]
        db.session.commit()

        logger.log_to_console(
            "INFO", f"Updated profile for user ID: {current_user['id']}"
        )
        return jsonify({"message": "User profile updated successfully."}), 200

    except ValueError as val_err:
        logger.log_to_console(
            "ERROR", "Validation error during profile update.", details=str(val_err)
        )
        log_error(
            val_err, module="user_routes", meta_data={"user_id": current_user.get("id")}
        )
        return (
            format_error_response(
                status=400,
                error_code="INVALID_USER_DATA",
                message="The provided user data is invalid.",
                details=str(val_err),
            ),
            400,
        )
    except Exception as exc:
        logger.log_to_console(
            "ERROR", "Unexpected error updating user profile.", exc_info=exc
        )
        log_error(exc, module="user_routes")
        return (
            format_error_response(
                status=500,
                error_code="UPDATE_PROFILE_ERROR",
                message="An unexpected error occurred while updating the user profile.",
                details=str(exc),
            ),
            500,
        )
