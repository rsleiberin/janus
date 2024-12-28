from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Image(db.Model):
    """Model for storing image metadata."""
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), unique=True, nullable=False, index=True)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    bit_depth = db.Column(db.Integer, nullable=True)
    color_type = db.Column(db.String(50), nullable=True)
    compression_method = db.Column(db.String(50), nullable=True)
    image_metadata = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Image {self.filename}>"
