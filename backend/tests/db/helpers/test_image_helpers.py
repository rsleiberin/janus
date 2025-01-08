import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
from backend.db import db
from backend.db.helpers.image_helpers import ImageHelpers
from backend.utils.error_handling.db.errors import (
    ImageNotFoundError,
    ImageCreationError,
    ImageUpdateError,
    ImageDeletionError,
)

# Logger instance
from backend.utils.logger import CentralizedLogger
logger = CentralizedLogger()

@pytest.mark.usefixtures("function_db_setup")
def test_create_image():
    """
    Tests the creation of an image using ImageHelpers.create.
    """
    image_data = {"filename": "test_image.png", "width": 800, "height": 600}
    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log, \
         patch("backend.utils.logger.CentralizedLogger.log_to_db") as mock_db_log:
        image = ImageHelpers.create(image_data)

        # Verify logging
        mock_console_log.assert_called_with("INFO", "Image created successfully", image_data=image_data)
        mock_db_log.assert_called_with(
            level="INFO",
            message="Image created successfully",
            module="image_helpers",
            meta_data=image_data
        )

        assert image.id is not None, "Image was not assigned an ID."
        assert image.width == 800 and image.height == 600, "Image dimensions incorrect."

    # Test error handling for creation
    with pytest.raises(ImageCreationError):
        ImageHelpers.create(None)  # Pass invalid data


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_id():
    """
    Tests retrieving an image by its ID.
    """
    image_data = {"filename": "id_test.png", "width": 500, "height": 500}
    image = ImageHelpers.create(image_data)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        fetched_image = ImageHelpers.get_by_id(image.id)

        # Verify logging
        mock_console_log.assert_called_with("INFO", f"Retrieved image by ID: {image.id}", found=True)

        assert fetched_image is not None, "Fetched image is None."
        assert fetched_image.id == image.id, "Fetched ID doesn't match created image."

    # Test error handling for non-existent ID
    with pytest.raises(ImageNotFoundError, match="Image with ID .* not found."):
        ImageHelpers.get_by_id(9999)


@pytest.mark.usefixtures("function_db_setup")
def test_update_image():
    """
    Tests updating an existing image record.
    """
    initial_data = {"filename": "update_test.png", "width": 300, "height": 300}
    updated_data = {"width": 1024, "height": 768}
    image = ImageHelpers.create(initial_data)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log, \
         patch("backend.utils.logger.CentralizedLogger.log_to_db") as mock_db_log:
        updated_image = ImageHelpers.update(image.id, updated_data)

        # Verify logging
        mock_console_log.assert_called_with("INFO", f"Updated image with ID: {image.id}", updates=updated_data)
        mock_db_log.assert_called_with(
            level="INFO",
            message=f"Updated image with ID: {image.id}",
            module="image_helpers",
            meta_data={"image_id": image.id, "updates": updated_data}
        )

        assert updated_image.width == 1024, "Width did not update correctly."
        assert updated_image.height == 768, "Height did not update correctly."

    # Test error handling for non-existent ID
    with pytest.raises(ImageNotFoundError, match="Image with ID .* not found."):
        ImageHelpers.update(9999, updated_data)


@pytest.mark.usefixtures("function_db_setup")
def test_delete_image():
    """
    Tests deleting an image record by its ID.
    """
    image_data = {"filename": "delete_test.png", "width": 400, "height": 200}
    image = ImageHelpers.create(image_data)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log, \
         patch("backend.utils.logger.CentralizedLogger.log_to_db") as mock_db_log:
        ImageHelpers.delete(image.id)

        # Verify logging
        mock_console_log.assert_called_with("INFO", f"Deleted image with ID: {image.id}")
        mock_db_log.assert_called_with(
            level="INFO",
            message=f"Deleted image with ID: {image.id}",
            module="image_helpers",
            meta_data={"image_id": image.id}
        )

    # Test error handling for already deleted ID
    with pytest.raises(ImageNotFoundError, match="Image with ID .* not found."):
        ImageHelpers.delete(image.id)


@pytest.mark.usefixtures("function_db_setup")
def test_get_all_images():
    """
    Tests retrieving all image records.
    """
    ImageHelpers.create({"filename": "img1.png", "width": 100, "height": 200})
    ImageHelpers.create({"filename": "img2.png", "width": 200, "height": 400})

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        all_images = ImageHelpers.get_all()

        # Verify logging
        mock_console_log.assert_called_with("INFO", "Retrieved all images", count=2)

        assert len(all_images) == 2, f"Expected 2 images, got {len(all_images)}."


@pytest.mark.usefixtures("function_db_setup")
def test_filter_by():
    """
    Tests filtering images by a specific field.
    """
    ImageHelpers.create({"filename": "filter1.png", "width": 300, "height": 300, "color_type": "RGB"})
    ImageHelpers.create({"filename": "filter2.png", "width": 300, "height": 300, "color_type": "Grayscale"})

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        rgb_images = ImageHelpers.filter_by("color_type", "RGB")

        # Verify logging
        mock_console_log.assert_called_with("INFO", "Filtered images by color_type", value="RGB", count=1)

        assert len(rgb_images) == 1, f"Expected 1 RGB image, found {len(rgb_images)}."


@pytest.mark.usefixtures("function_db_setup")
def test_count_images():
    """
    Tests counting the number of image records.
    """
    ImageHelpers.create({"filename": "count1.png", "width": 100, "height": 100})
    ImageHelpers.create({"filename": "count2.png", "width": 200, "height": 200})

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        total = ImageHelpers.count()

        # Verify logging
        mock_console_log.assert_called_with("INFO", "Counted all images", count=2)

        assert total == 2, f"Expected 2 images, found {total}."


@pytest.mark.usefixtures("function_db_setup")
def test_get_images_by_metadata():
    """
    Tests retrieving images by specific metadata.
    """
    metadata_value = {"test_key": "test_value"}
    ImageHelpers.create({"filename": "metadata.png", "width": 800, "height": 600, "image_metadata": metadata_value})

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        results = ImageHelpers.get_by_metadata(metadata_value)

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO",
            "Retrieved images by metadata",
            metadata=metadata_value,
            count=1
        )

        assert len(results) == 1, "Expected exactly 1 image with the given metadata."
        assert results[0].filename == "metadata.png", "Wrong image returned for metadata filter."

@pytest.mark.usefixtures("function_db_setup")
def test_exists_image():
    """
    Tests checking if an image with a specific ID exists.
    """
    image = ImageHelpers.create({"filename": "exists_test.png", "width": 50, "height": 50})

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        exists = ImageHelpers.exists(image.id)

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO",
            f"Checked existence for image ID: {image.id}",
            exists=True
        )

        assert exists is True, "Expected the image to exist."

    # Test for non-existent ID
    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        exists = ImageHelpers.exists(9999)

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO",
            "Checked existence for image ID: 9999",
            exists=False
        )

        assert exists is False, "Expected the image not to exist."


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_filename():
    """
    Tests retrieving an image by filename.
    """
    filename = "search_by_filename.png"
    ImageHelpers.create({"filename": filename, "width": 640, "height": 480})

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        found_image = ImageHelpers.get_by_filename(filename)

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO",
            f"Retrieved image by filename: {filename}",
            found=True
        )

        assert found_image is not None, "Expected to find an image by filename."
        assert found_image.filename == filename, "Filename does not match."

    # Test for non-existent filename
    with pytest.raises(ImageNotFoundError, match=f"Image with filename .* not found."):
        ImageHelpers.get_by_filename("non_existent.png")


@pytest.mark.usefixtures("function_db_setup")
def test_get_images_by_date_range():
    """
    Tests retrieving images created within a specific date range.
    """
    now = datetime.utcnow()
    past_date = now - timedelta(days=2)
    future_date = now + timedelta(days=2)

    # Create images at different times
    older_image = ImageHelpers.create({"filename": "old.png", "width": 320, "height": 240})
    older_image.created_at = past_date
    db.session.commit()

    new_image = ImageHelpers.create({"filename": "new.png", "width": 640, "height": 480})

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        results = ImageHelpers.get_images_by_date_range(now - timedelta(days=1), now + timedelta(days=1))

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO",
            "Retrieved images by date range",
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=1),
            count=1
        )

        # Assert results
        assert len(results) == 1, f"Expected 1 image in date range, got {len(results)}."
        assert results[0].filename == "new.png", "Wrong image returned in date range."


@pytest.mark.usefixtures("function_db_setup")
def test_get_images_by_size():
    """
    Tests retrieving images larger than a specified size.
    """
    ImageHelpers.create({"filename": "small.png", "width": 100, "height": 100})
    ImageHelpers.create({"filename": "big.png", "width": 1920, "height": 1080})

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        large_images = ImageHelpers.get_images_by_size(1280, 720)

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO",
            "Retrieved images by size",
            min_width=1280,
            min_height=720,
            count=1
        )

        assert len(large_images) == 1, f"Expected 1 image >=1280x720, found {len(large_images)}."
        assert large_images[0].filename == "big.png", "Wrong image returned for size filter."
@pytest.mark.usefixtures("function_db_setup")
def test_update_image_error():
    """
    Tests that ImageUpdateError is raised if an error occurs during the update process.
    """
    initial_data = {"filename": "update_error_test.png", "width": 300, "height": 300}
    image = ImageHelpers.create(initial_data)

    # Simulate an update error with an invalid attribute
    invalid_data = {"invalid_field": "invalid_value"}

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log, \
         patch("backend.utils.logger.CentralizedLogger.log_to_db") as mock_db_log:
        with pytest.raises(ImageUpdateError, match="Invalid field: invalid_field"):
            ImageHelpers.update(image.id, invalid_data)

        # Verify logging of the error
        mock_console_log.assert_called_with(
            "ERROR",
            f"Invalid field: invalid_field",
            updates=invalid_data
        )
        mock_db_log.assert_called_with(
            level="ERROR",
            message=f"Invalid field: invalid_field",
            module="image_helpers",
            meta_data={"image_id": image.id, "updates": invalid_data}
        )
