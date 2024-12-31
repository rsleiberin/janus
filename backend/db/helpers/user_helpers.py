# user_helpers.py
from backend.db import db
from backend.models import User
from datetime import datetime

# User Model Helpers
class UserHelpers:

    @staticmethod
    def create(user_data):
        """Create a new user record."""
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_id(user_id):
        """Get a user by their ID."""
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        """Get a user by their email."""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def update(user_id, updated_data):
        """Update an existing user record."""
        user = User.query.get(user_id)
        if user:
            for key, value in updated_data.items():
                setattr(user, key, value)
            db.session.commit()
        return user

    @staticmethod
    def delete(user_id):
        """Delete a user by their ID."""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    @staticmethod
    def count():
        """Get the number of users."""
        return User.query.count()

    @staticmethod
    def exists(user_id):
        """Check if a user with a specific ID exists."""
        return User.query.filter_by(id=user_id).first() is not None