"""
Defines the User model for storing user information, including hashed passwords.
"""

from werkzeug.security import generate_password_hash, check_password_hash
from backend.db import db
from .base import BaseModel


class User(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Stores user credentials and basic profile information.

    Relationships:
        - images:  One-to-many with 'Image'.
        - logs:    One-to-many with 'Log' (optional).
        - security:One-to-many with 'Security' logs or events.
    """

    __tablename__ = "users"

    username = db.Column(db.String(255), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str) -> None:
        """Hashes the given password and stores it in password_hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Checks the provided password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"
