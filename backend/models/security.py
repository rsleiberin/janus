"""
Defines the Security model, tracking security-related events (e.g., failed logins).
"""

from backend.db import db
from .base import BaseModel


class Security(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Records security-related events for auditing (e.g., access attempts).

    Relationship:
        - user: The user associated with the security event.
    """

    __tablename__ = "security"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    module = db.Column(db.String(100), nullable=True)
    level = db.Column(db.String(50), nullable=True)
    security_metadata = db.Column(db.JSON, nullable=True)

    user = db.relationship("User", backref=db.backref("security", lazy=True))

    def __repr__(self) -> str:
        return (
            f"<Security '{self.action}' "
            f"- User {self.user_id} (Level: {self.level}, Module: {self.module})>"
        )
