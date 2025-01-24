"""
Base configuration for the Flask application.

This class includes common settings that are inherited by specific environment
configurations.
"""

import os


class BaseConfig:  # pylint: disable=too-few-public-methods
    """Base configuration with common settings."""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = False  # Tokens won't expire for testing purposes
    SQLALCHEMY_DATABASE_URI = None  # To be defined in child configurations
    DEBUG = False  # Default value; can be overridden in child classes
    TESTING = False  # Default value; can be overridden in child classes

    @classmethod
    def validate(cls):
        """Validate that all necessary configurations are set."""
        missing_keys = []
        if not cls.SECRET_KEY:
            missing_keys.append("SECRET_KEY")
        if not cls.JWT_SECRET_KEY:
            missing_keys.append("JWT_SECRET_KEY")
        if not cls.SQLALCHEMY_DATABASE_URI:
            missing_keys.append("SQLALCHEMY_DATABASE_URI")

        if missing_keys:
            raise ValueError(f"Missing required config keys: {', '.join(missing_keys)}")
