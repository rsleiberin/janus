"""
This module defines configuration classes for the Flask application, including:
- Config
- DevelopmentConfig
- TestingConfig
- ProductionConfig
"""

import os
from backend.utils.logger import CentralizedLogger


class Config:  # pylint: disable=too-few-public-methods
    """Base configuration."""

    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY", "fallback_insecure_key")  # pylint: disable=invalid-name
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False  # pylint: disable=invalid-name
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super_secret_jwt_key")  # pylint: disable=invalid-name
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")  # pylint: disable=invalid-name

        self.logger = CentralizedLogger("config", log_level=self.LOG_LEVEL)

    def validate(self):
        """Validates critical configurations."""
        if (
            isinstance(self, ProductionConfig)
            and not os.getenv("DATABASE_URL")
        ):
            self.logger.log_to_console(
                "ERROR", "DATABASE_URL must be set in the environment for production!"
            )
            raise ValueError("DATABASE_URL must be set in the environment for production!")


class DevelopmentConfig(Config):  # pylint: disable=too-few-public-methods
    """Development configuration."""

    def __init__(self):
        super().__init__()
        self.DEBUG = True  # pylint: disable=invalid-name
        self.JWT_SECRET_KEY = "dev_jwt_secret"  # pylint: disable=invalid-name

        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, "instance", "backend.db")
        self.SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"  # pylint: disable=invalid-name

        self.logger.log_to_console(
            "DEBUG", "Development DB URI set.", db_uri=self.SQLALCHEMY_DATABASE_URI
        )


class TestingConfig(Config):  # pylint: disable=too-few-public-methods
    """Testing configuration."""

    __test__ = False

    def __init__(self):
        super().__init__()
        self.TESTING = True  # pylint: disable=invalid-name
        self.JWT_SECRET_KEY = "test_jwt_secret"  # pylint: disable=invalid-name
        self.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # pylint: disable=invalid-name
        self.logger.log_to_console("DEBUG", "Testing DB URI set to in-memory SQLite.")


class ProductionConfig(Config):  # pylint: disable=too-few-public-methods
    """Production configuration."""

    def __init__(self):
        super().__init__()
        self.DEBUG = False  # pylint: disable=invalid-name
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # pylint: disable=invalid-name
        self.SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  # pylint: disable=invalid-name
        self.logger.log_to_console(
            "DEBUG",
            "Production DB URI set.",
            db_uri=self.SQLALCHEMY_DATABASE_URI
        )
