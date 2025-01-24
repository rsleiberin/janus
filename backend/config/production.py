# File: backend/config/production.py

import os
from .base import BaseConfig


class ProductionConfig(BaseConfig):  # pylint: disable=too-few-public-methods
    """Production configuration."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI", "sqlite:///backend/instance/backend.db"
    )
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your_production_jwt_secret_key")
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_production_secret_key")
