"""
Defines the ImageAnalysis model for storing computed analysis of a single image.
"""

from backend.db import db
from .base import BaseModel


class ImageAnalysis(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Stores computed analysis results (e.g., color palette, luminosity metrics)
    associated with a single Image.

    By default, 'uselist=False' implies a one-to-one relationship with 'Image'.
    If you want multiple analyses per image, remove 'uselist=False'.
    """

    __tablename__ = "image_analysis"

    image_id = db.Column(db.Integer, db.ForeignKey("images.id"), nullable=False)
    analysis_results = db.Column(db.JSON, nullable=False)

    image = db.relationship(
        "Image", backref=db.backref("analysis", uselist=False, lazy=True)
    )

    def __repr__(self) -> str:
        return f"<ImageAnalysis {self.id} for Image {self.image_id}>"
