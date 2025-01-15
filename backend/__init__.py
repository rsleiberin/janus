import os
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from backend.db import db
from backend.config import DevelopmentConfig  # Change to ProductionConfig as needed
from backend.models import *  # Import all models
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import format_error_response, handle_general_error

# Initialize logger for this module
logger = CentralizedLogger("backend_init")

# Initialize Flask-Migrate
migrate = Migrate()

def create_app():
    """Factory function to create and configure the Flask application."""
    logger.log_to_console("INFO", "Starting app creation...")
    app = Flask(__name__)

    # Log the created app instance
    logger.log_to_console("DEBUG", "Created Flask app instance", instance=str(app))

    # Correctly resolve the database file path
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "instance", "image_processing.db")
    logger.log_to_console("DEBUG", "Resolved database path", path=db_path)

    # Apply configuration
    app.config.from_object(DevelopmentConfig)  # Use DevelopmentConfig for local development
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "your_test_secret_key"  # Add a secure JWT secret key

    logger.log_to_console("DEBUG", "Database URI set", uri=app.config["SQLALCHEMY_DATABASE_URI"])

    # Initialize the database
    try:
        logger.log_to_console("INFO", "Initializing the database...")
        db.init_app(app)
        migrate.init_app(app, db)
        logger.log_to_console("INFO", "db.init_app() and migrate.init_app() completed successfully.")
    except Exception as e:
        logger.log_to_console("ERROR", "Error during database initialization", error=str(e))
        raise

    # Initialize JWTManager
    try:
        JWTManager(app)
        logger.log_to_console("INFO", "JWTManager initialized successfully.")
    except Exception as e:
        logger.log_to_console("ERROR", "Error initializing JWTManager", error=str(e))
        raise

    # Register JWT error handlers
    @app.errorhandler(NoAuthorizationError)
    def handle_no_authorization_error(e):
        return format_error_response(
            status=401,
            error_code="AUTHENTICATION_FAILED",
            message="Authentication failed. Please log in.",
            details=str(e),
        ), 401

    @app.errorhandler(InvalidHeaderError)
    def handle_invalid_header_error(e):
        return format_error_response(
            status=401,
            error_code="INVALID_AUTH_HEADER",
            message="The authentication header is invalid.",
            details=str(e),
        ), 401

    # Register a global error handler for unhandled exceptions
    @app.errorhandler(Exception)
    def handle_unhandled_exception(e):
        logger.log_to_console("ERROR", str(e), module="general")
        return handle_general_error(e)

    # Import and register blueprints
    try:
        from backend.routes.status_routes import status_bp
        from backend.routes.file_routes import file_bp
        from backend.routes.authentication_routes import auth_bp
        from backend.routes.user_routes import user_bp
        from backend.routes.admin_routes import admin_bp
        from backend.routes.error_and_health_monitoring_routes import error_and_health_bp
        from backend.routes.analytics_routes import analytics_bp
        from backend.routes.security_routes import security_bp  # Add the security blueprint

        logger.log_to_console("INFO", "Blueprints imported successfully.")
    except ImportError as e:
        logger.log_to_console("ERROR", "Error importing blueprints", error=str(e))
        raise

    try:
        app.register_blueprint(status_bp)
        app.register_blueprint(file_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(error_and_health_bp)
        app.register_blueprint(analytics_bp)
        app.register_blueprint(security_bp)  # Register the security blueprint
        logger.log_to_console("INFO", "Blueprints registered successfully.")
    except Exception as e:
        logger.log_to_console("ERROR", "Error registering blueprints", error=str(e))
        raise

    logger.log_to_console("INFO", "App creation complete.")
    return app
