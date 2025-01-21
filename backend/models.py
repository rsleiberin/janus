"""
This module defines SQLAlchemy models for the application, including:
- Image
- ImageAnalysis
- User
- Admin
- Log
- Analytics
- Security
"""

from datetime import datetime

from backend.db import db


class Image(db.Model):  # pylint: disable=too-few-public-methods
    """Model for storing image metadata."""

    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    bit_depth = db.Column(db.Integer, nullable=True)
    color_type = db.Column(db.String(50), nullable=True)
    compression_method = db.Column(db.String(50), nullable=True)
    image_metadata = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user = db.relationship("User", backref=db.backref("images", lazy=True))

    def __repr__(self):
        return f"<Image {self.filename}>"


class ImageAnalysis(db.Model):  # pylint: disable=too-few-public-methods
    """Model for storing analysis results linked to images."""

    __tablename__ = "image_analysis"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"), nullable=False)
    analysis_results = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    image = db.relationship(
        "Image", backref=db.backref("analysis", uselist=False, lazy=True)
    )

    def __repr__(self):
        return f"<ImageAnalysis {self.id} for Image {self.image_id}>"


class User(db.Model):  # pylint: disable=too-few-public-methods
    """Model for storing user information."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class Admin(db.Model):  # pylint: disable=too-few-public-methods
    """Model for admin users, extending User model."""

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    admin_level = db.Column(db.String(50), nullable=False)

    user = db.relationship(
        "User", backref=db.backref("admin_profile", uselist=False, lazy=True)
    )

    def __repr__(self):
        return f"<Admin id={self.id}, user_id={self.user_id}, level={self.admin_level}>"


class Log(db.Model):  # pylint: disable=too-few-public-methods
    """Model for storing logs of user actions."""

    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    module = db.Column(db.String(100), nullable=True)
    level = db.Column(db.String(50), nullable=True)
    log_metadata = db.Column(db.JSON, nullable=True)

    user = db.relationship("User", backref=db.backref("logs", lazy=True))

    def __repr__(self):
        return (
            f"<Log {self.action} - User {self.user_id} "
            f"at {self.timestamp} (Level: {self.level}, Module: {self.module})>"
        )


class Analytics(db.Model):  # pylint: disable=too-few-public-methods
    """Model for storing research and analytical data."""

    __tablename__ = "analytics"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.JSON, nullable=False)
    research_topic = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Analytics {self.created_at} - {self.research_topic}>"


class Security(db.Model):  # pylint: disable=too-few-public-methods
    """Model for storing security-related events for users."""

    __tablename__ = "security"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user = db.relationship("User", backref=db.backref("security", lazy=True))

    def __repr__(self):
        return f"<Security {self.action} - User {self.user_id} at {self.timestamp}>"
