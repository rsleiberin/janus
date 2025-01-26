"""
Unified Auth & Security Routes.
"""

# pylint: disable=broad-exception-caught,reimported,import-outside-toplevel,R1710

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from backend.db import db
from backend.models import User
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import (
    handle_general_error,
    handle_authentication_error,
    handle_validation_error,
)
from backend.utils.error_handling.exceptions import (
    AuthenticationError,
    ValidationError,
)


auth_bp = Blueprint("auth", __name__)
logger = CentralizedLogger("auth_routes")


@auth_bp.route("/register", methods=["POST"])
def register_user():
    """
    Register a new user.
    Required JSON: {"username": "...", "email": "...", "password": "..."}
    """
    try:
        data = request.get_json() or {}
        required_fields = ("username", "email", "password")
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing field: {field}.")

        hashed_pw = generate_password_hash(data["password"])
        new_user = User(
            username=data["username"], email=data["email"], password_hash=hashed_pw
        )
        db.session.add(new_user)
        db.session.commit()

        logger.log_to_console("INFO", f"User registered: {new_user.username}")
        return jsonify({"message": "User registered successfully."}), 201
    except IntegrityError:
        db.session.rollback()
        logger.log_to_console("ERROR", "Duplicate email/username.")
        return jsonify({"error": "Email or username already exists."}), 409
    except ValidationError as val_err:
        logger.log_to_console("WARNING", str(val_err))
        return handle_validation_error(details=str(val_err))
    except Exception as exc:
        logger.log_to_console("ERROR", "Error registering user.", exc_info=exc)
        return handle_general_error(exc)


@auth_bp.route("/login", methods=["POST"])
def login_user():
    """
    Log in a user (returns access and refresh tokens).
    Required JSON: {"email": "...", "password": "..."}
    """
    try:
        data = request.get_json() or {}
        if "email" not in data or "password" not in data:
            raise ValidationError("Missing email or password.")

        user = User.query.filter_by(email=data["email"]).first()
        if not user or not check_password_hash(user.password_hash, data["password"]):
            raise AuthenticationError("Invalid credentials.")

        identity = {"id": user.id, "email": user.email}
        new_access_token = create_access_token(identity=identity)
        new_refresh_token = create_refresh_token(identity=identity)

        logger.log_to_console("INFO", f"User logged in: {user.email}")
        return (
            jsonify(
                {"access_token": new_access_token, "refresh_token": new_refresh_token}
            ),
            200,
        )
    except ValidationError as val_err:
        logger.log_to_console("WARNING", str(val_err))
        return handle_validation_error(details=str(val_err))
    except AuthenticationError as auth_err:
        logger.log_to_console("WARNING", str(auth_err))
        return handle_authentication_error(details=str(auth_err))
    except Exception as exc:
        logger.log_to_console("ERROR", "Error logging in user.", exc_info=exc)
        return handle_general_error(exc)


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Log out the current user (no DB logic by default).
    """
    try:
        current_user = get_jwt_identity()
        logger.log_to_console("INFO", f"User {current_user['email']} logged out.")
        return jsonify({"message": "Logout successful."}), 200
    except Exception as exc:
        logger.log_to_console("ERROR", "Error during logout.", exc_info=exc)
        return handle_general_error(exc)


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_jwt_token():
    """
    Refresh the user's access token using a valid refresh token.
    """
    try:
        current_user = get_jwt_identity()
        new_access = create_access_token(identity=current_user)
        logger.log_to_console("INFO", f"Token refreshed for {current_user['email']}")
        return jsonify({"access_token": new_access}), 200
    except Exception as exc:
        logger.log_to_console("ERROR", "Error refreshing token.", exc_info=exc)
        return handle_general_error(exc)


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    """
    Initiate a password reset (stub).
    Required JSON: {"email": "..."}
    """
    try:
        data = request.get_json() or {}
        if "email" not in data:
            raise ValidationError("Email is required for password reset.")

        logger.log_to_console("INFO", f"Reset password request for {data['email']}")
        return jsonify({"message": "Password reset email sent."}), 200
    except ValidationError as val_err:
        logger.log_to_console("WARNING", str(val_err))
        return handle_validation_error(details=str(val_err))
    except Exception as exc:
        logger.log_to_console("ERROR", "Error resetting password.", exc_info=exc)
        return handle_general_error(exc)


@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    """
    Change the current user's password.
    Required JSON: {"old_password": "...", "new_password": "..."}
    """
    try:
        current_user = get_jwt_identity()
        data = request.get_json() or {}
        old_pwd = data.get("old_password")
        new_pwd = data.get("new_password")
        if not old_pwd or not new_pwd:
            raise ValidationError("old_password and new_password are required.")

        user = db.session.get(User, current_user["id"])
        if not user:
            raise AuthenticationError("User does not exist.")
        if not check_password_hash(user.password_hash, old_pwd):
            raise AuthenticationError("Old password is incorrect.")
        if len(new_pwd) < 8:
            raise ValidationError("New password must be at least 8 characters long.")

        user.password_hash = generate_password_hash(new_pwd)
        db.session.commit()

        logger.log_to_console("INFO", f"Password changed for {current_user['email']}")
        return jsonify({"message": "Password changed successfully."}), 200
    except ValidationError as val_err:
        logger.log_to_console("WARNING", str(val_err))
        return handle_validation_error(details=str(val_err))
    except AuthenticationError as auth_err:
        logger.log_to_console("WARNING", str(auth_err))
        return handle_authentication_error(details=str(auth_err))
    except Exception as exc:
        logger.log_to_console("ERROR", "Error changing password.", exc_info=exc)
        return handle_general_error(exc)


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected_route():
    """
    A test route to verify JWT works.
    """
    try:
        current_user = get_jwt_identity()
        return jsonify({"message": f"Welcome {current_user['email']}!"}), 200
    except Exception as exc:
        logger.log_to_console("ERROR", "Error accessing protected route.", exc_info=exc)
        return handle_general_error(exc)
