from backend.db import db
from backend.models import User
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger("user_helpers")

class UserHelpers:
    @staticmethod
    def create(user_data):
        """Create a new user record."""
        try:
            user = User(**user_data)
            db.session.add(user)
            db.session.commit()
            logger.log_to_console("INFO", "User created successfully", user_id=user.id)
            return user
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to create user", error=str(e), user_data=user_data)
            db.session.rollback()
            return None

    @staticmethod
    def get_by_id(user_id):
        """Get a user by their ID."""
        try:
            user = db.session.get(User, user_id)
            logger.log_to_console("INFO", "Fetched user by ID", user_id=user_id, found=user is not None)
            return user
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to fetch user by ID", error=str(e), user_id=user_id)
            return None

    @staticmethod
    def get_by_email(email):
        """Get a user by their email."""
        try:
            user = db.session.query(User).filter_by(email=email).first()
            logger.log_to_console("INFO", "Fetched user by email", email=email, found=user is not None)
            return user
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to fetch user by email", error=str(e), email=email)
            return None

    @staticmethod
    def update(user_id, updated_data):
        """Update an existing user record."""
        try:
            user = db.session.get(User, user_id)
            if user:
                for key, value in updated_data.items():
                    setattr(user, key, value)
                db.session.commit()
                logger.log_to_console("INFO", "User updated successfully", user_id=user_id, updated_data=updated_data)
            else:
                logger.log_to_console("WARNING", "User not found for update", user_id=user_id)
            return user
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to update user", error=str(e), user_id=user_id, updated_data=updated_data)
            db.session.rollback()
            return None

    @staticmethod
    def delete(user_id):
        """Delete a user by their ID."""
        try:
            user = db.session.get(User, user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                logger.log_to_console("INFO", "User deleted successfully", user_id=user_id)
            else:
                logger.log_to_console("WARNING", "User not found for deletion", user_id=user_id)
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to delete user", error=str(e), user_id=user_id)
            db.session.rollback()

    @staticmethod
    def count():
        """Get the number of users."""
        try:
            count = db.session.query(User).count()
            logger.log_to_console("INFO", "Counted users", count=count)
            return count
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to count users", error=str(e))
            return 0

    @staticmethod
    def exists(user_id):
        """Check if a user with a specific ID exists."""
        try:
            exists = db.session.query(User).filter_by(id=user_id).first() is not None
            logger.log_to_console("INFO", "Checked if user exists", user_id=user_id, exists=exists)
            return exists
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to check if user exists", error=str(e), user_id=user_id)
            return False
