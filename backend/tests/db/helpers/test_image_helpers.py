# test_image_helpers.py

import pytest
import logging
from datetime import datetime, timedelta
from backend.db import db
from backend.db.helpers.image_helpers import ImageHelpers
from backend.models import Image

# Configure console logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("test_logger")


@pytest.mark.usefixtures("function_db_setup")
def test_create_image():
    """
    Tests the creation of an image using ImageHelpers.create.
    """
    logger.debug("Starting test_create_image...")

    image_data = {
        "filename": "test_image.png",
        "width": 800,
        "height": 600
    }
    image = ImageHelpers.create(image_data)
    logger.debug("[CREATE_IMAGE] Created image: %s", image)

    assert image.id is not None, "Image was not assigned an ID."
    assert image.width == 800 and image.height == 600, "Image dimensions incorrect."
    logger.debug("test_create_image passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_id():
    """
    Tests retrieving an image by its ID.
    """
    logger.debug("Starting test_get_by_id...")

    image_data = {
        "filename": "id_test.png",
        "width": 500,
        "height": 500
    }
    image = ImageHelpers.create(image_data)
    db.session.flush()

    fetched_image = ImageHelpers.get_by_id(image.id)
    logger.debug("[GET_BY_ID] Fetched image: %s", fetched_image)

    assert fetched_image is not None, "Fetched image is None."
    assert fetched_image.id == image.id, "Fetched ID doesn't match created image."
    logger.debug("test_get_by_id passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_update_image():
    """
    Tests updating an existing image record.
    """
    logger.debug("Starting test_update_image...")

    initial_data = {
        "filename": "update_test.png",
        "width": 300,
        "height": 300
    }
    updated_data = {
        "width": 1024,
        "height": 768
    }
    image = ImageHelpers.create(initial_data)
    logger.debug("[UPDATE_IMAGE] Created image: %s", image)

    updated_image = ImageHelpers.update(image.id, updated_data)
    logger.debug("[UPDATE_IMAGE] Updated image: %s", updated_image)

    assert updated_image.width == 1024, "Width did not update correctly."
    assert updated_image.height == 768, "Height did not update correctly."
    logger.debug("test_update_image passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_delete_image():
    """
    Tests deleting an image record by its ID.
    """
    logger.debug("Starting test_delete_image...")

    image_data = {
        "filename": "delete_test.png",
        "width": 400,
        "height": 200
    }
    image = ImageHelpers.create(image_data)
    logger.debug("[DELETE_IMAGE] Created image: %s", image)

    ImageHelpers.delete(image.id)
    logger.debug("[DELETE_IMAGE] Image deleted.")

    # Verify deletion
    deleted_image = ImageHelpers.get_by_id(image.id)
    logger.debug("[DELETE_IMAGE] Fetched after delete: %s", deleted_image)

    assert deleted_image is None, "Image record still present after deletion."
    logger.debug("test_delete_image passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_all_images():
    """
    Tests retrieving all image records.
    """
    logger.debug("Starting test_get_all_images...")

    ImageHelpers.create({"filename": "img1.png", "width": 100, "height": 200})
    ImageHelpers.create({"filename": "img2.png", "width": 200, "height": 400})

    all_images = ImageHelpers.get_all()
    logger.debug("[GET_ALL_IMAGES] All images: %s", all_images)

    assert len(all_images) == 2, f"Expected 2 images, got {len(all_images)}."
    logger.debug("test_get_all_images passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_filter_by():
    """
    Tests filtering images by a specific field.
    """
    logger.debug("Starting test_filter_by...")

    ImageHelpers.create({"filename": "filter1.png", "width": 300, "height": 300, "color_type": "RGB"})
    ImageHelpers.create({"filename": "filter2.png", "width": 300, "height": 300, "color_type": "Grayscale"})

    rgb_images = ImageHelpers.filter_by("color_type", "RGB")
    logger.debug("[FILTER_BY] Found %d RGB images.", len(rgb_images))

    assert len(rgb_images) == 1, f"Expected 1 RGB image, found {len(rgb_images)}."
    logger.debug("test_filter_by passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_count_images():
    """
    Tests counting the number of image records.
    """
    logger.debug("Starting test_count_images...")

    ImageHelpers.create({"filename": "count1.png", "width": 100, "height": 100})
    ImageHelpers.create({"filename": "count2.png", "width": 200, "height": 200})

    total = ImageHelpers.count()
    logger.debug("[COUNT_IMAGES] Total images: %d", total)

    assert total == 2, f"Expected 2 images, found {total}."
    logger.debug("test_count_images passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_exists_image():
    """
    Tests checking if an image with a specific ID exists.
    """
    logger.debug("Starting test_exists_image...")

    image = ImageHelpers.create({"filename": "exists_test.png", "width": 50, "height": 50})
    exists = ImageHelpers.exists(image.id)
    logger.debug("[EXISTS_IMAGE] Exists result: %s", exists)

    assert exists is True, "Expected the image to exist."
    logger.debug("test_exists_image passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_filename():
    """
    Tests retrieving an image by filename.
    """
    logger.debug("Starting test_get_by_filename...")

    filename = "search_by_filename.png"
    ImageHelpers.create({"filename": filename, "width": 640, "height": 480})

    found_image = ImageHelpers.get_by_filename(filename)
    logger.debug("[GET_BY_FILENAME] Found image: %s", found_image)

    assert found_image is not None, "Expected to find an image by filename."
    assert found_image.filename == filename, "Filename does not match."
    logger.debug("test_get_by_filename passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_images_by_date_range():
    """
    Tests retrieving images created within a specific date range.
    """
    logger.debug("Starting test_get_images_by_date_range...")

    now = datetime.utcnow()
    past_date = now - timedelta(days=2)
    future_date = now + timedelta(days=2)

    # Create images at different times
    older_image = ImageHelpers.create({"filename": "old.png", "width": 320, "height": 240})
    older_image.created_at = past_date
    db.session.commit()

    new_image = ImageHelpers.create({"filename": "new.png", "width": 640, "height": 480})

    # Query images created from yesterday to tomorrow
    results = ImageHelpers.get_images_by_date_range(now - timedelta(days=1), now + timedelta(days=1))
    logger.debug("[GET_IMAGES_BY_DATE_RANGE] Results: %s", results)

    # Expect only new_image in range
    assert len(results) == 1, f"Expected 1 image in date range, got {len(results)}."
    assert results[0].filename == "new.png", "Wrong image returned in date range."
    logger.debug("test_get_images_by_date_range passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_images_by_size():
    """
    Tests retrieving images larger than a specified size.
    """
    logger.debug("Starting test_get_images_by_size...")

    ImageHelpers.create({"filename": "small.png", "width": 100, "height": 100})
    ImageHelpers.create({"filename": "big.png", "width": 1920, "height": 1080})

    large_images = ImageHelpers.get_images_by_size(1280, 720)
    logger.debug("[GET_IMAGES_BY_SIZE] Found: %s", large_images)

    assert len(large_images) == 1, f"Expected 1 image >=1280x720, found {len(large_images)}."
    assert large_images[0].filename == "big.png", "Wrong image returned for size filter."
    logger.debug("test_get_images_by_size passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_metadata():
    """
    Tests retrieving images by specific metadata.
    """
    logger.debug("Starting test_get_by_metadata...")

    metadata_value = {"test_key": "test_value"}
    ImageHelpers.create({"filename": "metadata.png", "width": 800, "height": 600, "image_metadata": metadata_value})

    results = ImageHelpers.get_by_metadata(metadata_value)
    logger.debug("[GET_BY_METADATA] Found: %s", results)

    assert len(results) == 1, "Expected exactly 1 image with the given metadata."
    assert results[0].filename == "metadata.png", "Wrong image returned for metadata filter."
    logger.debug("test_get_by_metadata passed successfully.")
