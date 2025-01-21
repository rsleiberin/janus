from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User, db
from backend.utils.error_handling.error_handling import format_error_response, log_error
from backend.utils.logger import CentralizedLogger

# Initialize the logger
logger = CentralizedLogger("user_routes")

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_user_profile():
    """
    Retrieve the profile of the currently authenticated user.

    Returns:
        JSON response containing the user's profile information.
    """
    try:
        current_user = get_jwt_identity()
        user = db.session.get(User, current_user["id"])
        if not user:
            raise ValueError("User not found.")

        logger.log_to_console("INFO", f"Fetched profile for user ID: {current_user['id']}")
        return jsonify({"username": user.username, "email": user.email}), 200

    except ValueError as e:
        logger.log_to_console("WARNING", "User not found.", details=str(e))
        log_error(e, module="user_routes", meta_data={"user_id": current_user.get("id")})
        return (
            format_error_response(
                status=404,
                error_code="USER_NOT_FOUND",
                message="The requested user could not be found.",
                details=str(e),
            ),
            404,
        )

    except Exception as e:
        logger.log_to_console("ERROR", "Unexpected error fetching user profile.", exc_info=e)
        log_error(e, module="user_routes")
        return (
            format_error_response(
                status=500,
                error_code="FETCH_PROFILE_ERROR",
                message="An unexpected error occurred while fetching the user profile.",
                details=str(e),
            ),
            500,
        )


@user_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_user_profile():
    """
    Update the profile of the currently authenticated user.

    Returns:
        JSON response confirming the update.
    """
    try:
        current_user = get_jwt_identity()
        user = db.session.get(User, current_user["id"])
        if not user:
            raise ValueError("User not found.")

        data = request.json
        if not data or "username" not in data:
            raise ValueError("Invalid user data.")

        user.username = data["username"]
        db.session.commit()

        logger.log_to_console("INFO", f"Updated profile for user ID: {current_user['id']}")
        return jsonify({"message": "User profile updated successfully."}), 200

    except ValueError as e:
        logger.log_to_console("ERROR", "Validation error during profile update.", details=str(e))
        log_error(e, module="user_routes", meta_data={"user_id": current_user.get("id")})
        return (
            format_error_response(
                status=400,
                error_code="INVALID_USER_DATA",
                message="The provided user data is invalid.",
                details=str(e),
            ),
            400,
        )

    except Exception as e:
        logger.log_to_console("ERROR", "Unexpected error updating user profile.", exc_info=e)
        log_error(e, module="user_routes")
        return (
            format_error_response(
                status=500,
                error_code="UPDATE_PROFILE_ERROR",
                message="An unexpected error occurred while updating the user profile.",
                details=str(e),
            ),
            500,
        )
