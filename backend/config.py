import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')  # Secret key for securing sessions
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance reasons

class DevelopmentConfig(Config):
    """Development configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///backend/instance/image_processing.db'  # SQLite for local dev
    DEBUG = True
    print(f"Database URI: {SQLALCHEMY_DATABASE_URI}")


class ProductionConfig(Config):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # Production DB URL from env var
    DEBUG = False
