import os
from backend.utils.logger import CentralizedLogger

class Config:
    """Base configuration."""
    def __init__(self):
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_insecure_key')
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")  # Default to DEBUG

        # Set up centralized logger with dynamic log level
        self.logger = CentralizedLogger("config", log_level=self.LOG_LEVEL)

    def validate(self):
        """Validates critical configurations."""
        if self.SECRET_KEY == 'fallback_insecure_key':
            self.logger.log_to_console("WARNING", "Using an insecure SECRET_KEY. Set it in your environment.")
        if isinstance(self, ProductionConfig) and not os.getenv('DATABASE_URL'):
            self.logger.log_to_console("ERROR", "DATABASE_URL must be set in the environment for production!")
            raise ValueError("DATABASE_URL must be set in the environment for production!")

class DevelopmentConfig(Config):
    """Development configuration."""
    def __init__(self):
        super().__init__()
        self.DEBUG = True

        # Resolve the DB path relative to the backend directory
        base_dir = os.path.abspath(os.path.dirname(__file__))  # Current directory of config.py
        backend_dir = os.path.abspath(os.path.join(base_dir, "."))  # Backend directory
        db_path = os.path.join(backend_dir, "instance", "image_processing.db")
        self.SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

        # Log the resolved DB path
        self.logger.log_to_console("DEBUG", "Development DB URI set.", db_uri=self.SQLALCHEMY_DATABASE_URI)

class TestingConfig(Config):
    """Testing configuration."""
    __test__ = False  # Tell pytest not to collect this class as a test

    def __init__(self):
        super().__init__()
        self.TESTING = True
        self.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        self.logger.log_to_console("DEBUG", "Testing DB URI set to in-memory SQLite.")

class ProductionConfig(Config):
    """Production configuration."""
    def __init__(self):
        super().__init__()
        self.DEBUG = False
        self.SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
        self.logger.log_to_console("DEBUG", "Production DB URI set.", db_uri=self.SQLALCHEMY_DATABASE_URI)
