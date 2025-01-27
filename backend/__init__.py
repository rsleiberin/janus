"""
This module initializes the Flask application, sets up configurations,
and registers extensions for the backend.
"""

from flask import Flask
from flask_migrate import Migrate
from backend.db import db
from backend.config import config_by_name
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import handle_general_error
from backend.routes import register_blueprints

# Initialize logger
logger = CentralizedLogger("backend_init")

# Initialize Flask-Migrate
migrate = Migrate()


def create_app(config_name="development", testing=False):
    """Factory function to create and configure the Flask application."""
    logger.log_to_console("INFO", "Starting app creation...")
    app = Flask(__name__)

    if testing:
        config_name = "testing"

    config_class = config_by_name.get(config_name)
    if not config_class:
        raise ValueError(
            f"Invalid config name '{config_name}'. Available configs: "
            f"{list(config_by_name.keys())}"
        )

    app.config.from_object(config_class)
    logger.log_to_console("INFO", f"Loaded {config_name.capitalize()}Config.")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    register_blueprints(app)

    # Register global error handler
    @app.errorhandler(Exception)
    def handle_unhandled_exception(e):
        logger.log_to_console("ERROR", str(e), module="general")
        return handle_general_error(e)

    logger.log_to_console("INFO", "App creation complete.")
    return app
