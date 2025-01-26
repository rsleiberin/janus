# File: backend/db/helpers/image_helpers.py
# pylint: disable=R1710,W0718

from datetime import datetime
from typing import List
from backend.db.helpers.base_crud import BaseCrudHelper
from backend.models import Image
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import handle_database_error

logger = CentralizedLogger("image_helpers")


class ImageHelpers(BaseCrudHelper):
    """
    CRUD + specialized queries for Image model.
    """

    model = Image

    @staticmethod
    def get_images_by_size(min_width: int, min_height: int) -> List[Image]:
        """
        Retrieve images larger than specified dimensions.
        """
        try:
            images = Image.query.filter(
                Image.width >= min_width, Image.height >= min_height
            ).all()
            logger.log_to_console(
                "INFO",
                f"Retrieved {len(images)} images >= {min_width}x{min_height}.",
            )
            return images
        except Exception as err:
            handle_database_error(err, module="image_helpers")

    @staticmethod
    def get_images_by_date_range(
        start_date: datetime, end_date: datetime
    ) -> List[Image]:
        """
        Retrieve images created within a date range.
        """
        try:
            images = Image.query.filter(
                Image.created_at.between(start_date, end_date)
            ).all()
            logger.log_to_console(
                "INFO",
                f"Retrieved {len(images)} images between {start_date} and {end_date}.",
            )
            return images
        except Exception as err:
            handle_database_error(
                err,
                module="image_helpers",
                meta_data={
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                },
            )
