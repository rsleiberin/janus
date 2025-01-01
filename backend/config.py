import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')  # Secret key for securing sessions
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance reasons

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

    # Build an absolute path for the SQLite file, ensuring no relative path issues
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DB_PATH = os.path.join(BASE_DIR, "instance", "image_processing.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"

    print(f"Development DB URI: {SQLALCHEMY_DATABASE_URI}")

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # Production DB URL from env var
