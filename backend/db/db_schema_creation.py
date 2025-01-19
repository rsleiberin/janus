from backend.utils.logger import CentralizedLogger
from backend.db.db_setup import create_app
from backend.db import db
from sqlalchemy import inspect
from backend.utils.error_handling.db.errors import SchemaCreationError

logger = CentralizedLogger()


def create_schema():
    """Function to create the database schema."""
    app = create_app()
    with app.app_context():
        try:
            logger.log_to_console("DEBUG", "Creating database schema...")
            db.create_all()  # Create tables defined in models.py
            db.session.commit()
            logger.log_to_console("DEBUG", "Database schema created successfully.")
            logger.log_to_db(
                level="INFO",
                message="Database schema created successfully",
                module="db_schema_creation",
            )

            # Optional: Inspect tables for debugging
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            logger.log_to_console("DEBUG", f"Tables in the database: {tables}")
            logger.log_to_db(
                level="DEBUG",
                message="Tables inspected in the database",
                module="db_schema_creation",
                meta_data={"tables": tables},
            )
        except Exception as error:
            raise SchemaCreationError("Error while creating the schema.") from error


if __name__ == "__main__":
    create_schema()
