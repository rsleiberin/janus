import os
import pytest
from backend.utils.file_handler import (
    construct_file_path,
    is_valid_filename,
    read_file,
    write_file,
    delete_file,
)
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.exceptions import FileHandlerError

logger = CentralizedLogger(name="test_file_handler")


@pytest.mark.usefixtures("function_db_setup")
class TestFileHandler:
    """
    Tests for the file_handler module functions.
    """

    def test_is_valid_filename_success(self):
        assert is_valid_filename("test_file.txt") is True, "Filename should be valid."

    def test_is_valid_filename_failure(self):
        # Using '..' or '/' should be invalid per the regex
        assert is_valid_filename("../secret.txt") is False, "Filename with '..' should be invalid."
        assert is_valid_filename("some/dir/file.txt") is False, "Filename with '/' should be invalid."

    def test_construct_file_path(self):
        user_id = "test_user"
        filename = "test.txt"
        path = construct_file_path(user_id, filename)
        assert user_id in path, "Constructed path should include 'user_test_user'."
        assert filename in path, "Constructed path should include filename."

    def test_write_and_read_file(self, tmp_path):
        """
        Test writing and then reading a file.
        We override UPLOAD_FOLDER to a temp directory to avoid local clutter.
        """
        original_folder = os.getenv("UPLOAD_FOLDER", "")
        os.environ["UPLOAD_FOLDER"] = str(tmp_path)

        user_id = "test_user"
        filename = "sample.txt"
        content = b"Hello World!"

        write_file(user_id, filename, content, mode="wb")
        data = read_file(user_id, filename)
        assert data == content, "Read file content should match written content."

        # Clean up
        delete_file(user_id, filename)
        os.environ["UPLOAD_FOLDER"] = original_folder

    def test_write_file_invalid_filename(self):
        with pytest.raises(FileHandlerError, match="Invalid filename"):
            write_file("test_user", "../secret.txt", b"data")

    def test_read_nonexistent_file(self):
        with pytest.raises(FileHandlerError, match="File does not exist"):
            read_file("no_such_user", "no_such_file.txt")

    def test_delete_nonexistent_file(self):
        # Should log a warning but not raise an exception
        delete_file("random_user", "nonexistent.txt")
