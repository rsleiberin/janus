import os

class Config:
    """Base configuration with common settings."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "your_default_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your_jwt_secret_key")
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = False  # Tokens won't expire for testing purposes

    def validate(self):
        """Validate that all necessary configurations are set."""
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set.")
        if not self.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY must be set.")
        if not self.SQLALCHEMY_DATABASE_URI:
            raise ValueError("SQLALCHEMY_DATABASE_URI must be set.")
