# File: backend/utils/file_handler.py

import os
import re
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import ErrorContext, log_error
from backend.utils.error_handling.exceptions import FileHandlerError

# Logger setup
logger = CentralizedLogger(name="file_handler_logger")

# Configurable UPLOAD_FOLDER
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "backend/uploads")


def construct_file_path(user_id, filename):
    """
    Constructs the full file path for a given user and filename.
    Uses UPLOAD_FOLDER environment variable for path resolution.

    Args:
        user_id (str): The user ID.
        filename (str): The filename.

    Returns:
        str: The full file path.
    """
    base_folder = os.getenv("UPLOAD_FOLDER", "backend/uploads")
    user_folder = os.path.join(base_folder, f"user_{user_id}")
    return os.path.join(user_folder, filename)


def is_valid_filename(filename):
    """
    Validates the filename to prevent malicious or invalid paths.

    Args:
        filename (str): The filename to validate.

    Returns:
        bool: True if the filename is valid, False otherwise.
    """
    return not re.search(r"(\.\.|\/)", filename)


def read_file(user_id, filename):
    """
    Reads the contents of a file in text mode (UTF-8).

    Args:
        user_id (str): The ID of the user.
        filename (str): The name of the file.

    Returns:
        str: The contents of the file.

    Raises:
        FileHandlerError: If the file does not exist or cannot be read.
    """
    file_path = construct_file_path(user_id, filename)
    with ErrorContext(
        module="file_handler", meta_data={"operation": "read", "file_path": file_path}
    ):
        if not os.path.exists(file_path):
            raise FileHandlerError(f"File does not exist: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = f.read()
            logger.log_to_console("INFO", f"File read successfully: {file_path}")
            return data
        except Exception as e:
            log_error(e, module="file_handler", meta_data={"file_path": file_path})
            raise FileHandlerError(f"Failed to read file: {file_path}") from e


def write_file(user_id, filename, content, mode="w"):
    """
    Writes content to a file. If mode is binary (e.g., "wb"), omit encoding.

    Args:
        user_id (str): The ID of the user.
        filename (str): The name of the file.
        content (str/bytes): The data to write.
        mode (str, optional): File open mode, defaults to "w" (text).
                              Use "wb" for binary data (e.g., images).

    Raises:
        FileHandlerError: If the filename is invalid or the file cannot be written.
    """
    if not is_valid_filename(filename):
        raise FileHandlerError(f"Invalid filename: {filename}")

    file_path = construct_file_path(user_id, filename)
    user_directory = os.path.dirname(file_path)

    with ErrorContext(
        module="file_handler", meta_data={"operation": "write", "file_path": file_path}
    ):
        if not os.path.exists(user_directory):
            os.makedirs(user_directory)  # Ensure the user's directory exists
        try:
            # Omit encoding if in binary mode
            if "b" in mode:
                with open(file_path, mode, encoding="utf-8") as f:
                    f.write(content)  # content should be bytes
            else:
                with open(file_path, mode, encoding="utf-8") as f:
                    f.write(content)  # content should be string

            logger.log_to_console("INFO", f"File written successfully: {file_path}")
        except Exception as e:
            log_error(e, module="file_handler", meta_data={"file_path": file_path})
            raise FileHandlerError(f"Failed to write file: {file_path}") from e


def delete_file(user_id, filename):
    """
    Deletes a file if it exists.

    Args:
        user_id (str): The ID of the user.
        filename (str): The name of the file.

    Raises:
        FileHandlerError: If the file cannot be deleted.
    """
    file_path = construct_file_path(user_id, filename)
    with ErrorContext(
        module="file_handler", meta_data={"operation": "delete", "file_path": file_path}
    ):
        if not os.path.exists(file_path):
            logger.log_to_console(
                "WARNING", f"File does not exist for deletion: {file_path}"
            )
            return
        try:
            os.remove(file_path)
            logger.log_to_console("INFO", f"File deleted successfully: {file_path}")
        except Exception as e:
            log_error(e, module="file_handler", meta_data={"file_path": file_path})
            raise FileHandlerError(f"Failed to delete file: {file_path}") from e
