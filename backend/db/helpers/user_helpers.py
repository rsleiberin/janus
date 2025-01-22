# File: backend/db/helpers/user_helpers.py

from sqlalchemy.exc import SQLAlchemyError
from backend.db import db
from backend.models import User
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import (
    handle_database_error,
    handle_error_with_logging
)
from backend.utils.error_handling.exceptions import GeneralError

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
        except SQLAlchemyError as e:
            db.session.rollback()
            raise handle_database_error(
                e, module="user_helpers", meta_data={"user_data": user_data}
            )
        except Exception as e:
            db.session.rollback()
            raise handle_error_with_logging(
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
        except SQLAlchemyError as e:
            raise handle_database_error(
                e, module="user_helpers", meta_data={"user_id": user_id}
            )
        except ValueError as e:
            raise handle_error_with_logging(
                e, module="user_helpers", meta_data={"user_id": user_id}
            )
        except Exception as e:
            raise handle_error_with_logging(
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
        except SQLAlchemyError as e:
            raise handle_database_error(
                e, module="user_helpers", meta_data={"email": email}
            )
        except ValueError as e:
            raise handle_error_with_logging(
                e, module="user_helpers", meta_data={"email": email}
            )
        except Exception as e:
            raise handle_error_with_logging(
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
        except SQLAlchemyError as e:
            db.session.rollback()
            raise handle_database_error(
                e,
                module="user_helpers",
                meta_data={"user_id": user_id, "updated_data": updated_data},
            )
        except Exception as e:
            db.session.rollback()
            raise handle_error_with_logging(
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
        except SQLAlchemyError as e:
            db.session.rollback()
            raise handle_database_error(
                e, module="user_helpers", meta_data={"user_id": user_id}
            )
        except Exception as e:
            db.session.rollback()
            raise handle_error_with_logging(
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
        except SQLAlchemyError as e:
            raise handle_database_error(e, module="user_helpers")
        except Exception as e:
            raise handle_error_with_logging(e, module="user_helpers")

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
        except SQLAlchemyError as e:
            raise handle_database_error(
                e, module="user_helpers", meta_data={"user_id": user_id}
            )
        except Exception as e:
            raise handle_error_with_logging(
                e, module="user_helpers", meta_data={"user_id": user_id}
            )

    @staticmethod
    def get_user_by_nonexistent_field(value: str) -> None:
        """
        Attempt to get a user by a non-existent field to simulate a query error.
        """
        try:
            db.session.query(User).filter_by(nonexistent_field=value).all()
        except SQLAlchemyError as e:
            raise handle_database_error(
                e, module="user_helpers", meta_data={"query": "nonexistent_field"}
            )
        except Exception as e:
            raise handle_error_with_logging(
                e, module="user_helpers", meta_data={"query": "nonexistent_field"}
            )
