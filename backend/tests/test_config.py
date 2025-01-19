import pytest
from backend.config import DevelopmentConfig, TestingConfig, ProductionConfig
from backend.utils.logger import CentralizedLogger

# Set up logger for tests
logger = CentralizedLogger("test_logger", log_level="DEBUG")


def test_development_config(monkeypatch):
    """Test the DevelopmentConfig class."""
    # Mock the environment variable for SECRET_KEY
    monkeypatch.setenv("SECRET_KEY", "dev_secret_key")
    config = DevelopmentConfig()

    logger.log_to_console("DEBUG", "Testing DevelopmentConfig initialization.")

    assert config.DEBUG is True
    assert config.SECRET_KEY == "dev_secret_key"
    assert "sqlite" in config.SQLALCHEMY_DATABASE_URI  # Ensure SQLite is used


def test_testing_config():
    """Test the TestingConfig class."""
    config = TestingConfig()

    logger.log_to_console("DEBUG", "Testing TestingConfig initialization.")

    assert config.TESTING is True
    assert (
        config.SQLALCHEMY_DATABASE_URI == "sqlite:///:memory:"
    )  # Ensure in-memory SQLite is used


def test_production_config_missing_database_url(monkeypatch):
    """Test the ProductionConfig class with missing DATABASE_URL."""
    monkeypatch.delenv("DATABASE_URL", raising=False)  # Ensure DATABASE_URL is unset
    config = ProductionConfig()

    with pytest.raises(ValueError) as excinfo:
        config.validate()

    assert "DATABASE_URL must be set" in str(excinfo.value)


def test_production_config_with_database_url(monkeypatch):
    """Test the ProductionConfig class with a valid DATABASE_URL."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost/dbname")
    config = ProductionConfig()

    logger.log_to_console("DEBUG", "Testing ProductionConfig initialization.")
    config.validate()  # Ensure no exception is raised

    assert config.SQLALCHEMY_DATABASE_URI == "postgresql://user:pass@localhost/dbname"
