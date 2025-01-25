"""
Defines the Image model for storing metadata about uploaded images.
"""

from backend.db import db
from .base import BaseModel


class Image(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Stores details about an uploaded image.

    We enforce a unique constraint on (user_id, filename) so that each user can
    upload "my_photo.png" once, but different users can also use "my_photo.png"
    without collisions.

    Relationship:
        - user: Belongs to a single 'User' (images -> user).
        - analysis: One-to-one with 'ImageAnalysis' by default (uselist=False),
                    though you can allow multiple analyses if desired.
    """

    __tablename__ = "images"

    filename = db.Column(db.String(255), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    bit_depth = db.Column(db.Integer, nullable=True)
    color_type = db.Column(db.String(50), nullable=True)
    compression_method = db.Column(db.String(50), nullable=True)
    image_metadata = db.Column(db.JSON, nullable=True)

    # Create a unique constraint on (user_id, filename)
    __table_args__ = (
        db.UniqueConstraint("user_id", "filename", name="_user_filename_uc"),
    )

    user = db.relationship("User", backref=db.backref("images", lazy=True))

    def __repr__(self) -> str:
        return f"<Image {self.filename} (User {self.user_id})>"
