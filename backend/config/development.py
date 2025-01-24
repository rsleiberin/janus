# File: backend/config/development.py

import os
from .base import BaseConfig


class DevelopmentConfig(BaseConfig):  # pylint: disable=too-few-public-methods
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI", "sqlite:///backend/instance/backend.db"
    )
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your_development_jwt_secret_key")
