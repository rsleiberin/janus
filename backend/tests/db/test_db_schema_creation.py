import pytest
from sqlalchemy import inspect
from backend.db.db_schema_creation import create_schema
from backend.db import db
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.db.errors import SchemaCreationError

# Set up logger for tests
logger = CentralizedLogger("test_logger", log_level="DEBUG")

@pytest.mark.usefixtures("function_db_setup")
def test_create_schema():
    """
    Tests the create_schema function and validates table creation.
    """
    logger.log_to_console("DEBUG", "Starting test_create_schema...")

    try:
        create_schema()
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        logger.log_to_console("DEBUG", "Tables found", tables=tables)

        expected = {"users", "admins", "images", "logs", "analytics", "security"}
        missing = expected - set(tables)
        assert not missing, f"Missing tables: {missing}"

        logger.log_to_console("DEBUG", "test_create_schema passed successfully.")
    except SchemaCreationError as e:
        logger.log_to_console("ERROR", "SchemaCreationError caught in test", details=str(e))
        pytest.fail(f"SchemaCreationError: {str(e)}")
