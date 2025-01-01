# db_schema_creation.py

import logging
from backend.db.db_setup import create_app
from backend.db import db
from sqlalchemy import inspect

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_schema():
    """Function to create the database schema."""
    app = create_app()
    with app.app_context():
        logger.debug("Creating database schema...")
        db.create_all()  # Create tables defined in models.py
        db.session.commit()
        logger.debug("Database schema created successfully.")

        # Optional: Inspect tables for debugging
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        logger.debug(f"Tables in the database: {tables}")


if __name__ == "__main__":
    create_schema()
