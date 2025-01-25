"""
Defines the Analytics model for storing flexible JSON data on usage patterns.
"""

from backend.db import db
from .base import BaseModel


class Analytics(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Model for storing analytics or research data in JSON format.

    Example usage:
        - data might contain experiment results or aggregated metrics.
    """

    __tablename__ = "analytics"

    data = db.Column(db.JSON, nullable=False)
    research_topic = db.Column(db.String(255), nullable=True)

    def __repr__(self) -> str:
        return f"<Analytics {self.created_at} - {self.research_topic}>"
