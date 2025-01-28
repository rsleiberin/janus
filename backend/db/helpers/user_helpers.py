# File: backend/db/helpers/user_helpers.py

from sqlalchemy.exc import SQLAlchemyError
from backend.db.helpers.base_crud import BaseCrudHelper
from backend.models import User
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import (
    handle_database_error,
    handle_error_with_logging,
)

logger = CentralizedLogger("user_helpers")


class UserHelpers(BaseCrudHelper):
    """
    CRUD + specialized queries for User model.
    """

    model = User

    @staticmethod
    def get_by_email(email: str) -> User:
        """
        Get a user by their email.
        """
        if not email:
            raise ValueError("Email cannot be empty.")

        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                raise ValueError(f"User with email {email} not found.")
            logger.log_to_console("INFO", "User retrieved by email.", email=email)
            return user
        except SQLAlchemyError as err:
            handle_database_error(
                err, module="user_helpers", meta_data={"email": email}
            )
        except Exception as err:  # pylint: disable=W0718
            handle_error_with_logging(
                err, module="user_helpers", meta_data={"email": email}
            )

        # If admin, explicitly return None so that pylint sees "consistent return"
        return None

    @staticmethod
    def get_user_by_nonexistent_field(value: str):
        """
        Demonstrates an error if we query a non-existent column to test error handling.
        """
        try:
            User.query.filter_by(nonexistent_field=value).all()
        except SQLAlchemyError as err:
            handle_database_error(
                err,
                module="user_helpers",
                meta_data={"query": "nonexistent_field"},
            )
        except Exception as err:  # pylint: disable=W0718
            handle_error_with_logging(
                err,
                module="user_helpers",
                meta_data={"query": "nonexistent_field"},
            )
