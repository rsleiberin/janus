import os
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Config:
    """Base configuration."""
    def __init__(self):
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_insecure_key')
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance

    def validate(self):
        """Validates critical configurations."""
        if self.SECRET_KEY == 'fallback_insecure_key':
            logger.warning("Using an insecure SECRET_KEY. Set it in your environment.")
        if isinstance(self, ProductionConfig) and not os.getenv('DATABASE_URL'):
            raise ValueError("DATABASE_URL must be set in the environment for production!")

class DevelopmentConfig(Config):
    """Development configuration."""
    def __init__(self):
        super().__init__()
        self.DEBUG = True

        # Build an absolute path for the SQLite file, ensuring no relative path issues
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        db_path = os.path.join(base_dir, "instance", "image_processing.db")
        self.SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
        logger.debug(f"Development DB URI: {self.SQLALCHEMY_DATABASE_URI}")

class TestingConfig(Config):
    """Testing configuration."""
    __test__ = False  # Tell pytest not to collect this class as a test

    def __init__(self):
        super().__init__()
        self.TESTING = True
        self.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    """Production configuration."""
    def __init__(self):
        super().__init__()
        self.DEBUG = False
        self.SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
