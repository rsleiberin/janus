import os
import pytest


def test_production_config(monkeypatch):
    """Test the ProductionConfig class with valid DATABASE_URI."""
    # Mock environment variables before importing ProductionConfig
    monkeypatch.setenv("SECRET_KEY", "prod_secret_key")
    monkeypatch.setenv("DATABASE_URI", "postgresql://user:pass@localhost/dbname")
    monkeypatch.setenv("JWT_SECRET_KEY", "prod_jwt_secret_key")

    from backend.config.production import ProductionConfig

    class TestConfig(ProductionConfig):
        SECRET_KEY = os.getenv("SECRET_KEY")
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
        JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    config = TestConfig()

    assert config.DEBUG is False
    assert config.TESTING is False
    assert config.SECRET_KEY == "prod_secret_key"
    assert config.JWT_SECRET_KEY == "prod_jwt_secret_key"
    assert config.SQLALCHEMY_DATABASE_URI == "postgresql://user:pass@localhost/dbname"


def test_production_config_validation(monkeypatch):
    """Test the ProductionConfig class with missing DATABASE_URI."""
    # Ensure DATABASE_URI is unset before importing ProductionConfig
    monkeypatch.delenv("DATABASE_URI", raising=False)
    monkeypatch.setenv("SECRET_KEY", "prod_secret_key")
    monkeypatch.setenv("JWT_SECRET_KEY", "prod_jwt_secret_key")

    from backend.config.production import ProductionConfig

    class TestConfig(ProductionConfig):
        SECRET_KEY = os.getenv("SECRET_KEY")
        JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")

    config = TestConfig()

    with pytest.raises(ValueError) as excinfo:
        config.validate()
    assert "Missing required config keys: SQLALCHEMY_DATABASE_URI" in str(excinfo.value)

