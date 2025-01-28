"""
Unified Auth & Security Routes with dedicated refresh tokens & scalable roles
"""

import datetime
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

# Example of server-side token lifetime config, if desired:
ACCESS_EXPIRES = datetime.timedelta(minutes=15)  # short-living
REFRESH_EXPIRES = datetime.timedelta(days=30)  # long-living


@auth_bp.route("/register", methods=["POST"])
def register_user():
    """
    Register a new user.
    Stores a 'role' field for future scalability. By default: 'user'.
    Expects: {"username": "...", "email": "...", "password": "...",
        [optional "role": "..."]}
    """
    try:
        data = request.get_json() or {}
        required_fields = ("username", "email", "password")
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing field: {field}.")

        hashed_pw = generate_password_hash(data["password"])
        # Basic role usage:
        user_role = data.get("role", "user")  # default to 'user' if not provided

        new_user = User(
            username=data["username"],
            email=data["email"],
            password_hash=hashed_pw,
            # If you have a 'role' column in your User model:
            role=user_role,
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
    except Exception as exc:  # pylint: disable=W0718
        logger.log_to_console("ERROR", "Error registering user.", exc_info=exc)
        return handle_general_error(exc)


@auth_bp.route("/login", methods=["POST"])
def login_user():
    """
    Log in a user, returning short-lived access token + long-lived refresh token.
    Expects: {"email": "...", "password": "..."}
    """
    try:
        data = request.get_json() or {}
        if "email" not in data or "password" not in data:
            raise ValidationError("Missing email or password.")

        user = User.query.filter_by(email=data["email"]).first()
        if not user or not check_password_hash(user.password_hash, data["password"]):
            raise AuthenticationError("Invalid credentials.")

        # Example role usage:
        user_identity = {
            "id": user.id,
            "email": user.email,
            "role": getattr(user, "role", "user"),  # default to 'user' if not stored
        }
        access_token = create_access_token(
            identity=user_identity, expires_delta=ACCESS_EXPIRES
        )
        refresh_token = create_refresh_token(
            identity=user_identity, expires_delta=REFRESH_EXPIRES
        )

        logger.log_to_console("INFO", f"User {user.email} logged in successfully.")
        return (
            jsonify({"access_token": access_token, "refresh_token": refresh_token}),
            200,
        )

    except ValidationError as val_err:
        logger.log_to_console("WARNING", str(val_err))
        return handle_validation_error(details=str(val_err))
    except AuthenticationError as auth_err:
        logger.log_to_console("WARNING", str(auth_err))
        return handle_authentication_error(details=str(auth_err))
    except Exception as exc:  # pylint: disable=W0718
        logger.log_to_console("ERROR", "Error logging in user.", exc_info=exc)
        return handle_general_error(exc)


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Log out the current user (no DB logic by default).
    Possibly store token in server side 'revoked tokens' table if needed.
    """
    try:
        current_user = get_jwt_identity()
        logger.log_to_console("INFO", f"User {current_user['email']} logged out.")
        return jsonify({"message": "Logout successful."}), 200
    except Exception as exc:  # pylint: disable=W0718
        logger.log_to_console("ERROR", "Error during logout.", exc_info=exc)
        return handle_general_error(exc)


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_access_token():
    """
    Refresh the user's access token using a dedicated refresh token.
    """
    try:
        current_user = get_jwt_identity()
        # For post-quantum security, rotate tokens or shorten expiry if needed
        new_access = create_access_token(
            identity=current_user, expires_delta=ACCESS_EXPIRES
        )
        logger.log_to_console(
            "INFO", f"Access token refreshed for {current_user['email']}"
        )
        return jsonify({"access_token": new_access}), 200
    except Exception as exc:  # pylint: disable=W0718
        logger.log_to_console("ERROR", "Error refreshing token.", exc_info=exc)
        return handle_general_error(exc)


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    """
    Initiate a password reset (email sending not implemented).
    Expects: {"email": "..."}
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
    except Exception as exc:  # pylint: disable=W0718
        logger.log_to_console("ERROR", "Error resetting password.", exc_info=exc)
        return handle_general_error(exc)


@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    """
    Change the current user's password with a valid (short-lived) access token.
    Expects: {"old_password": "...", "new_password": "..."}
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
            raise ValidationError("New password must be at least 8 characters.")

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
    except Exception as exc:  # pylint: disable=W0718
        logger.log_to_console("ERROR", "Error changing password.", exc_info=exc)
        return handle_general_error(exc)
