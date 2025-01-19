import os
import re
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import error_context, log_error
from backend.utils.error_handling.utils.errors import FileHandlerError

logger = CentralizedLogger(name="file_handler_logger")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "backend/uploads")


def construct_file_path(user_id, filename):
    base_folder = UPLOAD_FOLDER
    user_folder = os.path.join(base_folder, f"user_{user_id}")
    return os.path.join(user_folder, filename)


def is_valid_filename(filename):
    return not re.search(r"(\.\.|\/)", filename)


def read_file(user_id, filename):
    file_path = construct_file_path(user_id, filename)
    with error_context(
        module="file_handler", meta_data={"operation": "read", "file_path": file_path}
    ):
        if not os.path.exists(file_path):
            raise FileHandlerError(f"File does not exist: {file_path}")
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            logger.log_to_console("INFO", f"File read successfully: {file_path}")
            return data
        except Exception as e:
            log_error(e, module="file_handler", meta_data={"file_path": file_path})
            raise FileHandlerError(f"Failed to read file: {file_path}") from e


def write_file(user_id, filename, content, mode="wb"):
    if not is_valid_filename(filename):
        raise FileHandlerError(f"Invalid filename: {filename}")

    file_path = construct_file_path(user_id, filename)
    user_directory = os.path.dirname(file_path)

    with error_context(
        module="file_handler", meta_data={"operation": "write", "file_path": file_path}
    ):
        if not os.path.exists(user_directory):
            os.makedirs(user_directory)
        try:
            with open(file_path, mode) as f:
                f.write(content)
            logger.log_to_console("INFO", f"File written successfully: {file_path}")
        except Exception as e:
            log_error(e, module="file_handler", meta_data={"file_path": file_path})
            raise FileHandlerError(f"Failed to write file: {file_path}") from e


def delete_file(user_id, filename):
    file_path = construct_file_path(user_id, filename)
    with error_context(
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
