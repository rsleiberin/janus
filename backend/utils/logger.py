# This module will define logging helpers to ensure that error logging and other relevant events are captured efficiently.

import logging

def setup_logger():
    """
    Configures the logger for the application to ensure that logs are recorded with the necessary details.
    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger('app')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

def log_error(logger, message, exception=None):
    """
    Logs error messages with an optional exception stack trace.
    Args:
        logger (logging.Logger): The logger instance.
        message (str): The error message to log.
        exception (Exception, optional): The exception object to log.
    """
    if exception:
        logger.error(f"{message} - {str(exception)}")
    else:
        logger.error(message)

def log_info(logger, message):
    """
    Logs informational messages.
    Args:
        logger (logging.Logger): The logger instance.
        message (str): The message to log.
    """
    logger.info(message)