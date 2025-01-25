"""
Defines the Admin model, which extends the User model for administrative privileges.
"""

from backend.db import db
from .base import BaseModel


class Admin(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Admin model linking to a specific user, storing admin-related data.

    Typically, you could use a 'role' field in 'User' instead of a separate table.
    This model is useful if there's a large set of fields exclusive to admins.
    """

    __tablename__ = "admins"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    admin_level = db.Column(db.String(50), nullable=False)

    user = db.relationship(
        "User", backref=db.backref("admin_profile", uselist=False, lazy=True)
    )

    def __repr__(self) -> str:
        return f"<Admin id={self.id}, user_id={self.user_id}, level={self.admin_level}>"
