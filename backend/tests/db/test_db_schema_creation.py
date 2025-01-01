# backend/tests/db/test_db_schema_creation.py

import pytest
import logging
from sqlalchemy import inspect
from backend.db.db_schema_creation import create_schema

from backend.db import db

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("test_logger")


@pytest.mark.usefixtures("function_db_setup")
def test_create_schema():
    logger.debug("Starting test_create_schema...")
    create_schema()
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    logger.debug(f"Tables found: {tables}")

    expected = {"users", "admins", "images", "logs", "analytics", "security"}
    missing = expected - set(tables)
    assert not missing, f"Missing tables: {missing}"

    logger.debug("test_create_schema passed successfully.")
