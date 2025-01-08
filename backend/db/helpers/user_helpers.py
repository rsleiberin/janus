from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError
from backend.db import db
from backend.models import User
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.db.errors import (
    UserError,
    UserNotFoundError,
    UserQueryError,
    UserCreationError,
    UserUpdateError,
    UserDeletionError,
)

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
            raise UserCreationError(f"Error creating user: {str(e)}") from e

    @staticmethod
    def get_by_id(user_id):
        """Get a user by their ID."""
        try:
            user = db.session.get(User, user_id)
            if not user:
                raise UserNotFoundError(f"User with ID {user_id} not found.")
            logger.log_to_console("INFO", "Fetched user by ID", user_id=user_id, found=True)
            return user
        except InvalidRequestError as e:
            logger.log_to_console("ERROR", "Invalid query for get_by_id", error=str(e), user_id=user_id)
            raise UserQueryError(f"Invalid query in get_by_id: {str(e)}") from e
        except SQLAlchemyError as e:
            logger.log_to_console("ERROR", "Failed to fetch user by ID", error=str(e), user_id=user_id)
            raise UserQueryError(f"Query error while fetching user by ID: {user_id}") from e

    @staticmethod
    def get_by_email(email):
        """Get a user by their email."""
        try:
            if email is None:  # Add explicit validation
                raise UserQueryError("Email cannot be None.")
            user = db.session.query(User).filter_by(email=email).first()
            if not user:
                raise UserNotFoundError(f"User with email {email} not found.")
            logger.log_to_console("INFO", "Fetched user by email", email=email, found=True)
            return user
        except InvalidRequestError as e:
            logger.log_to_console("ERROR", "Invalid query for get_by_email", error=str(e), email=email)
            raise UserQueryError(f"Invalid query in get_by_email: {str(e)}") from e
        except SQLAlchemyError as e:
            logger.log_to_console("ERROR", "Failed to query user by email", error=str(e), email=email)
            raise UserQueryError(f"Query error while fetching user by email: {email}") from e

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
                return user
            else:
                raise UserNotFoundError(f"User with ID {user_id} not found for update.")
        except SQLAlchemyError as e:
            logger.log_to_console("ERROR", "Failed to update user", error=str(e), user_id=user_id, updated_data=updated_data)
            db.session.rollback()
            raise UserUpdateError(f"Error updating user: {user_id}") from e

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
                raise UserNotFoundError(f"User with ID {user_id} not found for deletion.")
        except SQLAlchemyError as e:
            logger.log_to_console("ERROR", "Failed to delete user", error=str(e), user_id=user_id)
            db.session.rollback()
            raise UserDeletionError(f"Error deleting user: {user_id}") from e

    @staticmethod
    def count():
        """Get the number of users."""
        try:
            count = db.session.query(User).count()
            logger.log_to_console("INFO", "Counted users", count=count)
            return count
        except SQLAlchemyError as e:
            logger.log_to_console("ERROR", "Failed to count users", error=str(e))
            raise UserQueryError("Error counting users.") from e

    @staticmethod
    def exists(user_id):
        """Check if a user with a specific ID exists."""
        try:
            exists = db.session.query(User).filter_by(id=user_id).first() is not None
            logger.log_to_console("INFO", "Checked if user exists", user_id=user_id, exists=exists)
            return exists
        except SQLAlchemyError as e:
            logger.log_to_console("ERROR", "Failed to check if user exists", error=str(e), user_id=user_id)
            raise UserQueryError(f"Error checking existence of user ID: {user_id}") from e
