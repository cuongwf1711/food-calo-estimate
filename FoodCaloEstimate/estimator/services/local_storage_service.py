"""Local storage service module."""

import os
import shutil

from django.conf import settings

from FoodCaloEstimate.estimator.constants.image_constants import (
    LOCAL_IMAGE_PATH,
    LOCAL_IMAGE_URL,
)
from FoodCaloEstimate.estimator.services.image_service import ImageService


class LocalStorageService:
    """Local storage service class."""

    def upload_image(self, image, *folder):
        """Upload image to folder."""
        location = os.path.join(settings.MEDIA_ROOT, *folder)
        file_name_on_server = ImageService.generate_unique_filename()
        local_path = os.path.join(location, file_name_on_server)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "wb") as f:
            image.seek(0)
            f.write(image.read())
        return {
            LOCAL_IMAGE_PATH: local_path,
            LOCAL_IMAGE_URL: local_path.replace(
                settings.MEDIA_ROOT, settings.MAIN_MEDIA_URL
            ),
        }
