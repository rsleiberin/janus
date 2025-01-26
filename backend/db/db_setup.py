# File: backend/db/db_setup.py

"""
Utility script for initializing a Flask app with DB connectivity.
Does NOT run db.create_all(). For schema creation, use `flask db upgrade`.
"""

import os
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.exceptions import DatabaseConnectionError
from backend.app import create_app

logger = CentralizedLogger()


def create_app_with_db(config_name="development"):
    """
    Factory function to create and configure the Flask application with DB connection.
    Rely on `flask db upgrade` for actual schema creation.

    Args:
        config_name (str): 'development' | 'testing' | 'production'

    Returns:
        Flask: Configured Flask application.
    """
    logger.log_to_console("DEBUG", f"Creating app with config: {config_name}...")
    app = create_app(config_name)

    try:
        with app.app_context():
            logger.log_to_console(
                "DEBUG", "App context initialized. DB connection available."
            )
    except Exception as err:
        logger.log_to_console(
            "ERROR", "Failed to connect to the database.", details=str(err)
        )
        raise DatabaseConnectionError("Failed to connect to the database.") from err

    return app


if __name__ == "__main__":
    environment = os.getenv("FLASK_ENV", "development")
    application = create_app_with_db(environment)
    logger.log_to_console(
        "INFO",
        f"App created under {environment} config. "
        "Remember to run `flask db upgrade` to migrate the schema.",
    )
