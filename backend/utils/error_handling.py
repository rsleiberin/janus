# error_handling.py
# Helpers to manage errors and logging in the system.

import logging
from flask import jsonify

# Setting up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_error(error):
    """Helper function to handle errors and send standardized error messages."""
    logging.error(f"Error occurred: {error}")
    response = {
        'status': 'error',
        'message': str(error)
    }
    return jsonify(response), 500

def log_error(message):
    """Helper function to log errors."""
    logging.error(message)

def log_warning(message):
    """Helper function to log warnings."""
    logging.warning(message)

def log_info(message):
    """Helper function to log informational messages."""
    logging.info(message)

def log_debug(message):
    """Helper function to log debugging messages."""
    logging.debug(message)
