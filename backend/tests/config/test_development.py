import os
import pytest


def test_development_config(monkeypatch):
    """Test the DevelopmentConfig class."""
    # Mock environment variables before importing DevelopmentConfig
    monkeypatch.setenv("SECRET_KEY", "dev_secret_key")
    monkeypatch.setenv("DATABASE_URI", "sqlite:///backend/instance/test_dev.db")
    monkeypatch.setenv("JWT_SECRET_KEY", "dev_jwt_secret_key")

    from backend.config.development import DevelopmentConfig

    class TestConfig(DevelopmentConfig):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
        SECRET_KEY = os.getenv("SECRET_KEY")
        JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    config = TestConfig()

    assert config.DEBUG is True
    assert config.TESTING is False  # Inherits from BaseConfig
    assert config.SECRET_KEY == "dev_secret_key"
    assert config.JWT_SECRET_KEY == "dev_jwt_secret_key"
    assert config.SQLALCHEMY_DATABASE_URI == "sqlite:///backend/instance/test_dev.db"
