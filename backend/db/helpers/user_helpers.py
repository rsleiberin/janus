from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError
from backend.db import db
from backend.models import User
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.db.errors import handle_database_error

logger = CentralizedLogger("user_helpers")


class UserHelpers:
    @staticmethod
    def create(user_data: dict) -> User:
        """
        Create a new user record.
        """
        if not user_data:
            raise ValueError("User data cannot be empty.")

        try:
            user = User(**user_data)
            db.session.add(user)
            db.session.commit()
            logger.log_to_console("INFO", "User created successfully.", user_id=user.id)
            return user
        except Exception as e:
            db.session.rollback()
            raise handle_database_error(
                e, module="user_helpers", meta_data={"user_data": user_data}
            )

    @staticmethod
    def get_by_id(user_id: int) -> User:
        """
        Get a user by their ID.
        """
        try:
            user = db.session.get(User, user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")
            logger.log_to_console("INFO", "User retrieved by ID.", user_id=user_id)
            return user
        except Exception as e:
            raise handle_database_error(
                e, module="user_helpers", meta_data={"user_id": user_id}
            )

    @staticmethod
    def get_by_email(email: str) -> User:
        """
        Get a user by their email.
        """
        if not email:
            raise ValueError("Email cannot be empty.")

        try:
            user = db.session.query(User).filter_by(email=email).first()
            if not user:
                raise ValueError(f"User with email {email} not found.")
            logger.log_to_console("INFO", "User retrieved by email.", email=email)
            return user
        except Exception as e:
            raise handle_database_error(
                e, module="user_helpers", meta_data={"email": email}
            )

    @staticmethod
    def update(user_id: int, updated_data: dict) -> User:
        """
        Update an existing user record.
        """
        if not updated_data:
            raise ValueError("Update data cannot be empty.")

        try:
            user = db.session.get(User, user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")

            for key, value in updated_data.items():
                setattr(user, key, value)

            db.session.commit()
            logger.log_to_console(
                "INFO", "User updated successfully.", user_id=user_id
            )
            return user
        except Exception as e:
            db.session.rollback()
            raise handle_database_error(
                e,
                module="user_helpers",
                meta_data={"user_id": user_id, "updated_data": updated_data},
            )

    @staticmethod
    def delete(user_id: int) -> None:
        """
        Delete a user by their ID.
        """
        try:
            user = db.session.get(User, user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")

            db.session.delete(user)
            db.session.commit()
            logger.log_to_console("INFO", "User deleted successfully.", user_id=user_id)
        except Exception as e:
            db.session.rollback()
            raise handle_database_error(
                e, module="user_helpers", meta_data={"user_id": user_id}
            )

    @staticmethod
    def count() -> int:
        """
        Get the total number of users.
        """
        try:
            total_users = db.session.query(User).count()
            logger.log_to_console("INFO", "Counted total users.", count=total_users)
            return total_users
        except Exception as e:
            raise handle_database_error(e, module="user_helpers")

    @staticmethod
    def exists(user_id: int) -> bool:
        """
        Check if a user with a specific ID exists.
        """
        try:
            exists = db.session.query(User).filter_by(id=user_id).first() is not None
            logger.log_to_console(
                "INFO", "Checked if user exists.", user_id=user_id, exists=exists
            )
            return exists
        except Exception as e:
            raise handle_database_error(
                e, module="user_helpers", meta_data={"user_id": user_id}
            )
