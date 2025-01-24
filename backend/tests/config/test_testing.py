import os
import pytest


def test_testing_config(monkeypatch):
    """Test the TestingConfig class."""
    # Mock environment variables before importing TestingConfig
    monkeypatch.setenv("SECRET_KEY", "test_secret_key")
    monkeypatch.setenv("DATABASE_URI", "sqlite:///backend/instance/test_testing.db")
    monkeypatch.setenv("JWT_SECRET_KEY", "test_jwt_secret_key")

    from backend.config.testing import TestingConfig

    class TestConfig(TestingConfig):
        SECRET_KEY = os.getenv("SECRET_KEY")
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
        JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    config = TestConfig()

    assert config.DEBUG is False
    assert config.TESTING is True
    assert config.SECRET_KEY == "test_secret_key"
    assert config.JWT_SECRET_KEY == "test_jwt_secret_key"
    assert config.SQLALCHEMY_DATABASE_URI == "sqlite:///backend/instance/test_testing.db"
