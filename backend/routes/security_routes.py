from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    create_refresh_token,
)
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models import User, db
from backend.utils.error_handling.error_handling import format_error_response, log_error
from backend.utils.logger import CentralizedLogger

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
            raise ValueError("Email and password are required.")

        user = User.query.filter_by(email=data["email"]).first()
        if not user or not check_password_hash(user.password_hash, data["password"]):
            raise ValueError("Invalid email or password.")

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
    except ValueError as e:
        logger.log_to_console("WARNING", str(e))
        log_error(e, module="security_routes")
        return (
            format_error_response(
                status=401,
                error_code="AUTHENTICATION_ERROR",
                message="Authentication failed.",
                details=str(e),
            ),
            401,
        )
    except Exception as e:
        logger.log_to_console("ERROR", "Error during login.", exc_info=e)
        log_error(e, module="security_routes")
        return (
            format_error_response(
                status=500,
                error_code="LOGIN_ERROR",
                message="An unexpected error occurred during login.",
                details=str(e),
            ),
            500,
        )


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
        logger.log_to_console("ERROR", "Error during logout.", exc_info=e)
        log_error(e, module="security_routes")
        return (
            format_error_response(
                status=500,
                error_code="LOGOUT_ERROR",
                message="An unexpected error occurred during logout.",
                details=str(e),
            ),
            500,
        )


@security_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_access_token():
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
        logger.log_to_console("ERROR", "Error refreshing token.", exc_info=e)
        log_error(e, module="security_routes")
        return (
            format_error_response(
                status=500,
                error_code="REFRESH_TOKEN_ERROR",
                message="An unexpected error occurred while refreshing the token.",
                details=str(e),
            ),
            500,
        )


@security_bp.route("/reset-password", methods=["POST"])
def reset_password():
    """
    Send a password reset email to the user.
    """
    try:
        data = request.json
        if not data or "email" not in data:
            raise ValueError("Email is required.")

        logger.log_to_console(
            "INFO", f"Password reset requested for email: {data['email']}."
        )
        # Note: Add actual email sending logic here
        return jsonify({"message": "Password reset email sent."}), 200
    except ValueError as e:
        logger.log_to_console("WARNING", str(e))
        log_error(e, module="security_routes")
        return (
            format_error_response(
                status=400,
                error_code="INVALID_EMAIL",
                message="A valid email address is required.",
                details=str(e),
            ),
            400,
        )
    except Exception as e:
        logger.log_to_console("ERROR", "Error during password reset.", exc_info=e)
        log_error(e, module="security_routes")
        return (
            format_error_response(
                status=500,
                error_code="RESET_PASSWORD_ERROR",
                message="An unexpected error occurred during password reset.",
                details=str(e),
            ),
            500,
        )


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
            raise ValueError("Old and new passwords are required.")

        user = User.query.get(current_user["id"])
        if not user or not check_password_hash(
            user.password_hash, data["old_password"]
        ):
            raise ValueError("Old password is incorrect.")

        if len(data["new_password"]) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        user.password_hash = generate_password_hash(data["new_password"])
        db.session.commit()

        logger.log_to_console(
            "INFO", f"Password changed successfully for user {current_user['email']}."
        )
        return jsonify({"message": "Password changed successfully."}), 200
    except ValueError as e:
        logger.log_to_console("WARNING", str(e))
        log_error(e, module="security_routes")
        return (
            format_error_response(
                status=400,
                error_code="WEAK_PASSWORD",
                message="Password does not meet the requirements.",
                details=str(e),
            ),
            400,
        )
    except Exception as e:
        logger.log_to_console("ERROR", "Error changing password.", exc_info=e)
        log_error(e, module="security_routes")
        return (
            format_error_response(
                status=500,
                error_code="CHANGE_PASSWORD_ERROR",
                message="An unexpected error occurred while changing the password.",
                details=str(e),
            ),
            500,
        )


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
            "ERROR", "Error accessing protected route.", exc_info=e
        )
        log_error(e, module="security_routes")
        return (
            format_error_response(
                status=500,
                error_code="PROTECTED_ROUTE_ERROR",
                message="An unexpected error occurred while accessing the protected route.",
                details=str(e),
            ),
            500,
        )
