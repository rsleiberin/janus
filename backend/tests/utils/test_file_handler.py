# test_file_handler.py

import os
import pytest
from backend.utils.file_handler import read_file, write_file, delete_file
from backend.utils.error_handling.utils.errors import FileHandlerError

@pytest.mark.usefixtures("function_db_setup")
class TestFileHandler:
    """
    Tests for the file_handler module.
    """

    def test_read_nonexistent_file(self, tmp_path):
        """
        Attempt to read a file that doesn't exist.
        Expect a FileHandlerError.
        """
        non_existent_file = tmp_path / "non_existent.txt"
        with pytest.raises(FileHandlerError) as exc_info:
            read_file(str(non_existent_file))
        assert "File does not exist" in str(exc_info.value)

    def test_read_file_success(self, tmp_path):
        """
        Successfully read a file that exists.
        """
        file_path = tmp_path / "test_read.txt"
        file_content = "Hello, Janus!"
        file_path.write_text(file_content, encoding="utf-8")

        result = read_file(str(file_path))
        assert result == file_content

    def test_write_file_success(self, tmp_path):
        """
        Successfully write content to a file.
        """
        file_path = tmp_path / "test_write.txt"
        content_to_write = "Welcome to Janus!"
        
        write_file(str(file_path), content_to_write)
        assert file_path.read_text(encoding="utf-8") == content_to_write

    def test_write_file_exception(self, tmp_path):
        """
        Attempt to write to an invalid path, expecting FileHandlerError.
        """
        # On some operating systems, writing to a directory as a file triggers an error
        invalid_path = tmp_path  # This is a directory, not a file
        with pytest.raises(FileHandlerError):
            write_file(str(invalid_path), "Should fail")

    def test_delete_file_nonexistent(self, tmp_path):
        """
        Deleting a file that doesn't exist should not raise an error.
        It logs a warning but continues gracefully.
        """
        non_existent_file = tmp_path / "non_existent_delete.txt"
        delete_file(str(non_existent_file))  # Should not raise an exception

    def test_delete_file_success(self, tmp_path):
        """
        Successfully delete an existing file.
        """
        file_path = tmp_path / "test_delete.txt"
        file_path.write_text("Content to delete", encoding="utf-8")

        delete_file(str(file_path))
        assert not file_path.exists()
