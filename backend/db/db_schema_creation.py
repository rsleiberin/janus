from backend import create_app
from backend.db import db
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_schema():
    """Function to create the database schema."""
    app = create_app()

    # Create the database schema
    with app.app_context():
        logger.debug("Creating database schema...")
        db.create_all()  # Create tables defined in models.py
        db.session.commit()  # Commit changes
        logger.debug("Database schema created successfully.")

        # Optionally, check tables created (for debugging)
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        logger.debug(f"Tables in the database: {tables}")

if __name__ == "__main__":
    create_schema()
