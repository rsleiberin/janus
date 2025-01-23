import pytest
from unittest.mock import patch, ANY
from datetime import datetime, timedelta
from backend.db import db
from backend.db.helpers.image_helpers import ImageHelpers
from backend.models import Image
from backend.utils.error_handling.exceptions import ImageError  # Corrected import
from backend.utils.logger import CentralizedLogger

# Logger instance
logger = CentralizedLogger("test_image_helpers")


@pytest.mark.usefixtures("function_db_setup")
def test_create_image():
    image_data = {
        "filename": "test_image.png",
        "width": 800,
        "height": 600,
        "user_id": 1,
    }
    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_log:
        image = ImageHelpers.create(image_data)
        mock_log.assert_called_with(
            "INFO", "Image created successfully.", image_data=image_data
        )
        assert image.id is not None, "Image ID is missing after creation."


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_id():
    image_data = {
        "filename": "get_by_id.png",
        "width": 500,
        "height": 500,
        "user_id": 1,
    }
    image = ImageHelpers.create(image_data)
    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_log:
        fetched_image = ImageHelpers.get_by_id(image.id)
        mock_log.assert_called_with(
            "INFO",
            f"Retrieved image by ID: {image.id}",
        )
        assert fetched_image.id == image.id, "Fetched image ID does not match."


@pytest.mark.usefixtures("function_db_setup")
def test_update_image():
    initial_data = {
        "filename": "update_test.png",
        "width": 300,
        "height": 300,
        "user_id": 1,
    }
    image = ImageHelpers.create(initial_data)
    updated_data = {"width": 1024, "height": 768}

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_log:
        updated_image = ImageHelpers.update(image.id, updated_data)
        mock_log.assert_called_with(
            "INFO",
            f"Updated image with ID: {image.id}",
            updates=updated_data,
        )
        assert updated_image.width == 1024, "Image width not updated correctly."


@pytest.mark.usefixtures("function_db_setup")
def test_delete_image():
    image_data = {
        "filename": "delete_test.png",
        "width": 400,
        "height": 200,
        "user_id": 1,
    }
    image = ImageHelpers.create(image_data)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_log:
        ImageHelpers.delete(image.id)
        mock_log.assert_called_with(
            "INFO",
            f"Deleted image with ID: {image.id}",
        )
        # Verify deletion
        deleted_image = db.session.get(Image, image.id)
        assert deleted_image is None, "Image was not deleted."


@pytest.mark.usefixtures("function_db_setup")
def test_get_all_images():
    ImageHelpers.create(
        {"filename": "img1.png", "width": 100, "height": 200, "user_id": 1}
    )
    ImageHelpers.create(
        {"filename": "img2.png", "width": 200, "height": 400, "user_id": 1}
    )

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_log:
        all_images = ImageHelpers.get_all()
        mock_log.assert_called_with("INFO", "Retrieved all images.", count=2)
        assert len(all_images) == 2, "Expected 2 images but found a different count."


@pytest.mark.usefixtures("function_db_setup")
def test_exists_image():
    image = ImageHelpers.create(
        {"filename": "exists_test.png", "width": 50, "height": 50, "user_id": 1}
    )

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_log:
        exists = ImageHelpers.exists(image.id)
        mock_log.assert_called_with(
            "INFO",
            f"Checked existence for image ID: {image.id}",
            exists=True,
        )
        assert exists is True, "Image existence check failed."


@pytest.mark.usefixtures("function_db_setup")
def test_get_images_by_size():
    ImageHelpers.create(
        {"filename": "small.png", "width": 100, "height": 100, "user_id": 1}
    )
    ImageHelpers.create(
        {"filename": "big.png", "width": 1920, "height": 1080, "user_id": 1}
    )

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_log:
        large_images = ImageHelpers.get_images_by_size(1280, 720)
        mock_log.assert_called_with(
            "INFO", "Retrieved 1 images larger than 1280x720.", min_width=1280, min_height=720
        )
        assert len(large_images) == 1, "Expected 1 large image."


@pytest.mark.usefixtures("function_db_setup")
def test_get_images_by_date_range():
    now = datetime.utcnow()
    past_date = now - timedelta(days=2)

    # Create images with different timestamps
    older_image = ImageHelpers.create(
        {"filename": "old.png", "width": 320, "height": 240, "user_id": 1}
    )
    older_image.created_at = past_date
    db.session.commit()

    ImageHelpers.create(
        {"filename": "new.png", "width": 640, "height": 480, "user_id": 1}
    )

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_log:
        results = ImageHelpers.get_images_by_date_range(past_date, now)
        mock_log.assert_called_with(
            "INFO", "Retrieved 1 images within the date range.", start_date=past_date, end_date=now
        )
        assert len(results) == 1, "Expected 1 image in the date range."


@pytest.mark.usefixtures("function_db_setup")
def test_image_creation_failure():
    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_log:
        with pytest.raises(ImageError, match="Failed to create image."):
            ImageHelpers.create(None)
        mock_log.assert_called_with(
            "ERROR", "Failed to create image.", exception=ANY, image_data=None
        )
