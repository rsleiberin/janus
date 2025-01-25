"""
Defines the Log model for recording user or system actions.
"""

from backend.db import db
from .base import BaseModel


class Log(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Records high-level events and user actions.

    Potential usage:
        - 'action': short description of what happened.
        - 'module': which part of the system triggered the action.
        - 'level': severity or category (INFO, ERROR, etc.).
        - 'log_metadata': JSON for extended info.

    Relationship:
        - user: The user who performed the action (optional if e.g., system events).
    """

    __tablename__ = "logs"

    action = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    module = db.Column(db.String(100), nullable=True)
    level = db.Column(db.String(50), nullable=True)
    log_metadata = db.Column(db.JSON, nullable=True)

    user = db.relationship("User", backref=db.backref("logs", lazy=True))

    def __repr__(self) -> str:
        return (
            f"<Log '{self.action}' "
            f"- User {self.user_id} (Level: {self.level}, Module: {self.module})>"
        )
