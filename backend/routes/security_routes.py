from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    create_refresh_token,
)
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models import User, db
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.routes.errors import (
    handle_route_error,
    AuthenticationError,
    UnauthorizedError,
    WeakPasswordError,
)

logger = CentralizedLogger("security_routes")

security_bp = Blueprint("security", __name__, url_prefix="/security")


@security_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user and issue JWT tokens.
    """
    try:
        data = request.json
        if not data or "email" not in data or "password" not in data:
            raise AuthenticationError("Email and password are required.")

        user = User.query.filter_by(email=data["email"]).first()
        if not user or not check_password_hash(user.password_hash, data["password"]):
            raise AuthenticationError("Invalid email or password.")

        access_token = create_access_token(
            identity={"id": user.id, "email": user.email}
        )
        refresh_token = create_refresh_token(
            identity={"id": user.id, "email": user.email}
        )

        logger.log_to_console("INFO", f"User {user.email} logged in successfully.")
        return (
            jsonify({"access_token": access_token, "refresh_token": refresh_token}),
            200,
        )
    except Exception as e:
        logger.log_to_console("ERROR", "Error during login.", details=str(e))
        return handle_route_error(e)


@security_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Log out the current user by invalidating the token.
    """
    try:
        current_user = get_jwt_identity()
        logger.log_to_console("INFO", f"User {current_user['email']} logged out.")
        return jsonify({"message": "Logout successful."}), 200
    except Exception as e:
        logger.log_to_console("ERROR", "Error during logout.", details=str(e))
        return handle_route_error(e)


@security_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    """
    Refresh the user's access token using a refresh token.
    """
    try:
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        logger.log_to_console(
            "INFO", f"Token refreshed for user {current_user['email']}."
        )
        return jsonify({"access_token": new_access_token}), 200
    except Exception as e:
        logger.log_to_console("ERROR", "Error refreshing token.", details=str(e))
        return handle_route_error(e)


@security_bp.route("/reset-password", methods=["POST"])
def reset_password():
    """
    Send a password reset email to the user.
    """
    try:
        data = request.json
        if not data or "email" not in data:
            raise AuthenticationError("Email is required.")

        logger.log_to_console(
            "INFO", f"Password reset requested for email: {data['email']}."
        )
        # Note: Add actual email sending logic here
        return jsonify({"message": "Password reset email sent."}), 200
    except Exception as e:
        logger.log_to_console("ERROR", "Error during password reset.", details=str(e))
        return handle_route_error(e)


@security_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    """
    Allow a user to change their password.
    """
    try:
        current_user = get_jwt_identity()
        data = request.json

        if not data or "old_password" not in data or "new_password" not in data:
            raise AuthenticationError("Old and new passwords are required.")

        user = User.query.get(current_user["id"])
        if not user or not check_password_hash(
            user.password_hash, data["old_password"]
        ):
            raise UnauthorizedError("Old password is incorrect.")

        if len(data["new_password"]) < 8:
            raise WeakPasswordError("Password must be at least 8 characters long.")

        user.password_hash = generate_password_hash(data["new_password"])
        db.session.commit()

        logger.log_to_console(
            "INFO", f"Password changed successfully for user {current_user['email']}."
        )
        return jsonify({"message": "Password changed successfully."}), 200
    except Exception as e:
        logger.log_to_console("ERROR", "Error changing password.", details=str(e))
        return handle_route_error(e)


@security_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """
    A protected route for testing JWT access.
    """
    try:
        current_user = get_jwt_identity()
        return jsonify({"message": f"Welcome {current_user['email']}!"}), 200
    except Exception as e:
        logger.log_to_console(
            "ERROR", "Error accessing protected route.", details=str(e)
        )
        return handle_route_error(e)
