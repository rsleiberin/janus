"""
Defines the BaseModel class, an abstract model that adds common fields like 'id',
'created_at', and 'updated_at' to all derived models.
"""

from datetime import datetime
from backend.db import db


class BaseModel(db.Model):  # pylint: disable=too-few-public-methods
    """Abstract base class with common fields for all models."""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
