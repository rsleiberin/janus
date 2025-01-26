# File: backend/db/helpers/base_crud.py
# pylint: disable=R1710,W0718

"""
Defines a generic CRUD helper base class for any SQLAlchemy model.
Eliminates repetitive code across domain-specific helper classes.
"""

from backend.db import db
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import handle_database_error

logger = CentralizedLogger("base_crud")


class BaseCrudHelper:
    """
    Subclass must define:
        model = <SQLAlchemy model class>
    Example:
        class UserHelpers(BaseCrudHelper):
            model = User
    """

    model = None

    @classmethod
    def create(cls, data: dict):
        """
        Create a new record for cls.model.
        """
        try:
            record = cls.model(**data)  # pylint: disable=not-callable
            db.session.add(record)
            db.session.commit()
            logger.log_to_console(
                "INFO", f"{cls.model.__name__} created successfully.", data=data
            )
            return record
        except Exception as err:
            db.session.rollback()
            handle_database_error(err, module=cls.__name__, meta_data=data)

    @classmethod
    def get_by_id(cls, record_id: int):
        """
        Retrieve a record by ID.
        """
        try:
            record = db.session.get(cls.model, record_id)
            if not record:
                raise ValueError(f"{cls.model.__name__} ID {record_id} not found.")
            return record
        except Exception as err:
            handle_database_error(
                err, module=cls.__name__, meta_data={"record_id": record_id}
            )

    @classmethod
    def update(cls, record_id: int, updated_data: dict):
        """
        Update an existing record by ID.
        """
        try:
            record = db.session.get(cls.model, record_id)
            if not record:
                raise ValueError(f"{cls.model.__name__} ID {record_id} not found.")
            for key, value in updated_data.items():
                setattr(record, key, value)
            db.session.commit()
            logger.log_to_console(
                "INFO",
                f"{cls.model.__name__} ID {record_id} updated.",
                updates=updated_data,
            )
            return record
        except Exception as err:
            db.session.rollback()
            handle_database_error(
                err,
                module=cls.__name__,
                meta_data={"record_id": record_id, "updates": updated_data},
            )

    @classmethod
    def delete(cls, record_id: int):
        """
        Delete a record by ID.
        """
        try:
            record = db.session.get(cls.model, record_id)
            if not record:
                raise ValueError(f"{cls.model.__name__} ID {record_id} not found.")
            db.session.delete(record)
            db.session.commit()
            logger.log_to_console(
                "INFO", f"{cls.model.__name__} ID {record_id} deleted."
            )
        except Exception as err:
            db.session.rollback()
            handle_database_error(
                err, module=cls.__name__, meta_data={"record_id": record_id}
            )

    @classmethod
    def count(cls):
        """
        Return total number of records for this model.
        """
        try:
            total = db.session.query(cls.model).count()
            logger.log_to_console(
                "INFO", f"Counted {total} {cls.model.__name__} records."
            )
            return total
        except Exception as err:
            handle_database_error(err, module=cls.__name__)

    @classmethod
    def exists(cls, record_id: int) -> bool:
        """
        Check if a given record_id exists for this model.
        """
        try:
            return (
                db.session.query(cls.model).filter_by(id=record_id).first() is not None
            )
        except Exception as err:
            handle_database_error(
                err, module=cls.__name__, meta_data={"record_id": record_id}
            )
            return False
