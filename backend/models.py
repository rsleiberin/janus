from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from backend.db import db



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

class User(db.Model):
    """Model for storing user information."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # e.g., 'admin', 'user'

    def __repr__(self):
        return f"<User {self.username}>"

class Admin(db.Model):
    """Model for admin users, extending User model."""
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    admin_level = db.Column(db.String(50), nullable=False)  # e.g., 'superadmin', 'moderator'

    user = db.relationship('User', backref=db.backref('admins', lazy=True))

    def __repr__(self):
        # Avoid triggering a lazy-load after the session has closed.
        return f"<Admin id={self.id}, user_id={self.user_id}, level={self.admin_level}>"


class Log(db.Model):
    """Model for storing logs of user actions."""
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('logs', lazy=True))

    def __repr__(self):
        return f"<Log {self.action} - User {self.user.username} at {self.timestamp}>"

class Analytics(db.Model):
    """Model for storing research and analytical data."""
    __tablename__ = 'analytics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.JSON, nullable=False)
    research_topic = db.Column(db.String(255), nullable=True)  # Optional field to differentiate research
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Analytics {self.created_at} - {self.research_topic}>"

class Security(db.Model):
    """Model for storing security-related events for users."""
    __tablename__ = 'security'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('security', lazy=True))

    def __repr__(self):
        return f"<Security {self.action} - User {self.user.username} at {self.timestamp}>"

