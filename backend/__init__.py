"""
This module initializes the Flask application, sets up configurations,
and registers blueprints and extensions for the backend.
"""

import os
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from backend.db import db
from backend.config import DevelopmentConfig
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import (
    format_error_response,
    handle_general_error,
)

# Blueprints
from backend.routes.status_routes import status_bp
from backend.routes.file_routes import file_bp
from backend.routes.authentication_routes import auth_bp
from backend.routes.user_routes import user_bp
from backend.routes.admin_routes import admin_bp
from backend.routes.error_and_health_monitoring_routes import error_and_health_bp
from backend.routes.analytics_routes import analytics_bp
from backend.routes.security_routes import security_bp
from backend.routes.log_routes import log_bp
from backend.routes.image_routes import image_bp

# Initialize logger
logger = CentralizedLogger("backend_init")

# Initialize Flask-Migrate
migrate = Migrate(directory=os.path.join(os.path.dirname(__file__), "migrations"))


def configure_database(app):
    """Configure the database for the app."""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "instance", "backend.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def configure_jwt(app):
    """Configure JWT and error handlers."""
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def handle_no_authorization_error(e):
        return (
            format_error_response(
                status=401,
                error_code="AUTHENTICATION_FAILED",
                message="Authentication failed. Please log in.",
                details=e,
            ),
            401,
        )

    @jwt.invalid_token_loader
    def handle_invalid_token_error(e):
        return (
            format_error_response(
                status=401,
                error_code="INVALID_TOKEN",
                message="Token is invalid or expired.",
                details=e,
            ),
            401,
        )


def register_blueprints(app):
    """Register all blueprints."""
    app.register_blueprint(status_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(error_and_health_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(log_bp)
    app.register_blueprint(image_bp, url_prefix="/images")


def create_app():
    """Factory function to create and configure the Flask application."""
    logger.log_to_console("INFO", "Starting app creation...")
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    configure_database(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    configure_jwt(app)

    # Register global error handler
    @app.errorhandler(Exception)
    def handle_unhandled_exception(e):
        logger.log_to_console("ERROR", str(e), module="general")
        return handle_general_error(e)

    # Register blueprints
    register_blueprints(app)

    logger.log_to_console("INFO", "App creation complete.")
    return app
