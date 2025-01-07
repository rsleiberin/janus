import pytest
from backend.config import DevelopmentConfig, TestingConfig, ProductionConfig
from backend.utils.logger import CentralizedLogger


def test_development_config(monkeypatch, caplog):
    """Test the DevelopmentConfig class."""
    caplog.clear()
    logger = CentralizedLogger("test_logger")

    # Mock the environment variable for SECRET_KEY
    monkeypatch.setenv("SECRET_KEY", "dev_secret_key")
    config = DevelopmentConfig()
    with caplog.at_level("DEBUG"):
        logger.log_to_console("DEBUG", "Testing DevelopmentConfig initialization.")
    
    assert config.DEBUG is True
    assert config.SECRET_KEY == "dev_secret_key"
    assert "sqlite" in config.SQLALCHEMY_DATABASE_URI  # Ensure SQLite is used
    assert "Development DB URI set." in caplog.text  # Ensure logger output includes DB URI


def test_testing_config(caplog):
    """Test the TestingConfig class."""
    caplog.clear()
    logger = CentralizedLogger("test_logger")
    config = TestingConfig()
    
    with caplog.at_level("DEBUG"):
        logger.log_to_console("DEBUG", "Testing TestingConfig initialization.")

    assert config.TESTING is True
    assert config.SQLALCHEMY_DATABASE_URI == "sqlite:///:memory:"  # Ensure in-memory SQLite is used
    assert "Testing DB URI set to in-memory SQLite." in caplog.text


def test_production_config_missing_database_url(monkeypatch, caplog):
    """Test the ProductionConfig class with missing DATABASE_URL."""
    caplog.clear()
    logger = CentralizedLogger("test_logger")

    monkeypatch.delenv("DATABASE_URL", raising=False)  # Ensure DATABASE_URL is unset
    config = ProductionConfig()
    
    with pytest.raises(ValueError) as excinfo:
        config.validate()
    
    assert "DATABASE_URL must be set" in str(excinfo.value)
    assert "DATABASE_URL must be set in the environment for production!" in caplog.text


def test_production_config_with_database_url(monkeypatch, caplog):
    """Test the ProductionConfig class with a valid DATABASE_URL."""
    caplog.clear()
    logger = CentralizedLogger("test_logger")

    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost/dbname")
    config = ProductionConfig()
    
    with caplog.at_level("DEBUG"):
        config.validate()  # Ensure no exception is raised

    assert config.SQLALCHEMY_DATABASE_URI == "postgresql://user:pass@localhost/dbname"
    assert "Production DB URI set." in caplog.text
