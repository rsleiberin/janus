"""
Application factory for the Flask application.
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from backend.config import config_by_name

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name=None, testing=False):
    """
    Create and configure the Flask application.

    Args:
        config_name (str): The configuration name to use.
        testing (bool): If True, use the testing configuration.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Determine configuration
    if testing:
        config_name = "testing"
    elif config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    # Load configuration
    config_class = config_by_name.get(config_name)
    if not config_class:
        raise ValueError(
            f"Invalid config name '{config_name}'. Available configs: {list(config_by_name.keys())}"
        )

    app.config.from_object(config_class)
    app.config.from_pyfile("config.py", silent=True)

    # Validate configurations
    if hasattr(config_class, "validate"):
        config_class.validate()

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from backend.routes import register_blueprints
    register_blueprints(app)

    return app
