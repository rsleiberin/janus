# File: backend/config/testing.py

"""
Testing configuration for the Flask application.
"""

import os
from .base import BaseConfig


class TestingConfig(BaseConfig):  # pylint: disable=too-few-public-methods
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:////home/tank/janus/backend/config/instance/test_testing.db")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "test_jwt_secret_key")
    SECRET_KEY = os.environ.get("SECRET_KEY", "test_secret_key")
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing purposes
    DEBUG = False  # Explicitly set DEBUG for testing
