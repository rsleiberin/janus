from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from backend.db import db
from backend.models import User
from backend.utils.error_handling.error_handling import (
    handle_authentication_error,
    handle_unauthorized_error,
)
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger("authentication_routes")

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register_user():
    """
    Endpoint to register a new user.
    """
    try:
        data = request.get_json()
        # Removed "role" from required fields
        required_fields = ("username", "email", "password")
        if not data or not all(key in data for key in required_fields):
            raise ValueError("Missing required fields: username, email, or password.")

        hashed_password = generate_password_hash(data["password"])
        # Removed "role"
        new_user = User(
            username=data["username"],
            email=data["email"],
            password_hash=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()

        logger.log_to_console("INFO", f"User registered: {new_user.username}")
        return jsonify({"message": "User registered successfully."}), 201

    except IntegrityError:
        db.session.rollback()
        logger.log_to_console("ERROR", "Email or username already exists.")
        return jsonify({"error": "Email or username already exists."}), 409
    except ValueError as ve:
        logger.log_to_console("ERROR", str(ve))
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.log_to_console("ERROR", "Error registering user.", exc_info=e)
        return jsonify({"error": "An error occurred while registering the user."}), 500


@auth_bp.route("/login", methods=["POST"])
def login_user():
    """
    Endpoint to log in a user.
    """
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ("email", "password")):
            raise ValueError("Missing email or password.")

        user = User.query.filter_by(email=data["email"]).first()
        if not user or not check_password_hash(user.password_hash, data["password"]):
            return jsonify({"error": "Authentication error."}), 401

        # Identity just has id and username, no "role" in the DB
        access_token = create_access_token(
            identity={"id": user.id, "username": user.username}
        )
        logger.log_to_console("INFO", f"User logged in: {user.username}")
        return jsonify({"access_token": access_token}), 200

    except ValueError as ve:
        logger.log_to_console("ERROR", str(ve))
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.log_to_console("ERROR", "Error logging in user.", exc_info=e)
        return jsonify({"error": "An error occurred while logging in the user."}), 500


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def user_profile():
    try:
        current_user = get_jwt_identity()
        user = db.session.get(User, current_user["id"])

        if not user:
            return handle_unauthorized_error(details="User not found.")

        logger.log_to_console("INFO", f"Profile accessed: {user.username}")
        return (
            jsonify({"id": user.id, "username": user.username, "email": user.email}),
            200,
        )

    except Exception as e:
        logger.log_to_console("ERROR", "Error retrieving user profile.", exc_info=e)
        return handle_authentication_error(
            details="An error occurred while retrieving the user profile."
        )
