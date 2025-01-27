import os
import pytest


def test_base_config(monkeypatch):
    """Test the BaseConfig class."""
    # Mock environment variables before importing BaseConfig
    monkeypatch.setenv("SECRET_KEY", "base_secret_key")
    monkeypatch.setenv("JWT_SECRET_KEY", "base_jwt_secret_key")
    monkeypatch.setenv("DATABASE_URI", "sqlite:///backend/instance/base.db")

    from backend.config.base import BaseConfig

    # Ensure environment variables are being loaded correctly
    os.environ["SECRET_KEY"] = "base_secret_key"
    os.environ["JWT_SECRET_KEY"] = "base_jwt_secret_key"
    os.environ["DATABASE_URI"] = "sqlite:///backend/instance/base.db"

    class TestConfig(BaseConfig):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
        SECRET_KEY = os.getenv("SECRET_KEY")
        JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    config = TestConfig()

    assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False
    assert config.SECRET_KEY == "base_secret_key"
    assert config.JWT_SECRET_KEY == "base_jwt_secret_key"
    assert config.SQLALCHEMY_DATABASE_URI == "sqlite:///backend/instance/base.db"


def test_base_config_validation(monkeypatch):
    """Test the BaseConfig validation method."""
    # Mock environment variables with missing DATABASE_URI
    monkeypatch.setenv("SECRET_KEY", "base_secret_key")
    monkeypatch.setenv("JWT_SECRET_KEY", "base_jwt_secret_key")
    monkeypatch.delenv("DATABASE_URI", raising=False)

    from backend.config.base import BaseConfig

    class TestConfig(BaseConfig):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
        SECRET_KEY = os.getenv("SECRET_KEY")
        JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    config = TestConfig()

    with pytest.raises(ValueError) as excinfo:
        config.validate()
    assert "Missing required config keys: SQLALCHEMY_DATABASE_URI" in str(excinfo.value)
