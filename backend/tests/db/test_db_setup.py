# test_db_setup.py

import pytest
import logging
from flask import Flask
from backend.db.db_setup import create_app

from backend.db import db

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("test_logger")

def test_create_app():
    """
    Tests that create_app returns a Flask application with the expected configuration.
    """
    logger.debug("Starting test_create_app...")

    app = create_app()
    assert isinstance(app, Flask), "create_app did not return a Flask instance."

    # Check that the config is loaded
    assert "SQLALCHEMY_DATABASE_URI" in app.config, "Missing SQLALCHEMY_DATABASE_URI in config."
    logger.debug(f"Database URI from config: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Check that db is initialized
    with app.app_context():
        assert db.engine is not None, "Database engine was not initialized."

    logger.debug("test_create_app passed successfully.")
