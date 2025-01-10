from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User, db
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.routes.errors import handle_route_error, UserNotFoundError, InvalidUserDataError

logger = CentralizedLogger("user_routes")

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_user_profile():
    try:
        current_user = get_jwt_identity()
        # Use Session.get() instead of Query.get()
        user = db.session.get(User, current_user["id"])
        if not user:
            raise UserNotFoundError("User not found.")

        return jsonify({"username": user.username, "email": user.email}), 200
    except Exception as e:
        logger.log_to_console("ERROR", "Error fetching user profile", error=str(e))
        return handle_route_error(e)


@user_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_user_profile():
    try:
        current_user = get_jwt_identity()
        # Use Session.get() instead of Query.get()
        user = db.session.get(User, current_user["id"])
        if not user:
            raise UserNotFoundError("User not found.")

        data = request.json
        if not data or "username" not in data:
            raise InvalidUserDataError("Invalid user data.")

        user.username = data["username"]
        db.session.commit()

        return jsonify({"message": "User profile updated successfully."}), 200
    except Exception as e:
        logger.log_to_console("ERROR", "Error updating user profile", error=str(e))
        return handle_route_error(e)
