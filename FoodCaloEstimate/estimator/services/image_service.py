"""Image Service."""

import uuid
from datetime import datetime

from FoodCaloEstimate.estimator.constants.image_constants import FORMAT_IMAGE


class ImageService:
    """Image Service."""

    @staticmethod
    def generate_unique_filename(file_name="image_file", extension=FORMAT_IMAGE):
        """Generate a unique filename."""
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"{file_name}_{current_time}_{uuid.uuid4()}.{extension}"
