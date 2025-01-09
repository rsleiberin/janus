# file_handler.py

import os
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import error_context, log_error
from backend.utils.error_handling.utils.errors import FileHandlerError

logger = CentralizedLogger(name="file_handler_logger")

def read_file(file_path):
    """
    Reads the contents of a file.
    
    Args:
        file_path (str): The path to the file to read.

    Returns:
        str: Contents of the file.
    """
    with error_context(module="file_handler", meta_data={"operation": "read", "file_path": file_path}):
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

def write_file(file_path, content, mode="w"):
    """
    Writes content to a file.

    Args:
        file_path (str): Path to the file.
        content (str): The data to write.
        mode (str, optional): File open mode, defaults to "w" (write).
    """
    with error_context(module="file_handler", meta_data={"operation": "write", "file_path": file_path}):
        try:
            with open(file_path, mode, encoding="utf-8") as f:
                f.write(content)
            logger.log_to_console("INFO", f"File written successfully: {file_path}")
        except Exception as e:
            log_error(e, module="file_handler", meta_data={"file_path": file_path})
            raise FileHandlerError(f"Failed to write file: {file_path}") from e

def delete_file(file_path):
    """
    Deletes a file if it exists.

    Args:
        file_path (str): Path to the file to delete.
    """
    with error_context(module="file_handler", meta_data={"operation": "delete", "file_path": file_path}):
        if not os.path.exists(file_path):
            logger.log_to_console("WARNING", f"File does not exist for deletion: {file_path}")
            return
        try:
            os.remove(file_path)
            logger.log_to_console("INFO", f"File deleted successfully: {file_path}")
        except Exception as e:
            log_error(e, module="file_handler", meta_data={"file_path": file_path})
            raise FileHandlerError(f"Failed to delete file: {file_path}") from e
