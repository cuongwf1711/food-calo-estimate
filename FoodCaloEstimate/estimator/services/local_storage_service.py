"""Local storage service module."""

import os
import shutil

from django.conf import settings

from FoodCaloEstimate.estimator.constants.image_constants import (
    LOCAL_IMAGE_PATH,
    LOCAL_IMAGE_URL,
    ORIGIN_IMAGE,
    SEGMENTATION_IMAGE,
)
from FoodCaloEstimate.estimator.utils.generate_unique_filename import generate_unique_filename


class LocalStorageService:
    """Local storage service class."""

    def get_local_image_url(self, local_image_path, local_image_url):
        """Get the image URL."""
        return {
            LOCAL_IMAGE_PATH: local_image_path,
            LOCAL_IMAGE_URL: local_image_url,
        }

    def upload_image(self, image, *folder):
        """Upload image to folder."""
        location = os.path.join(settings.MEDIA_ROOT, *folder)
        file_name_on_server = generate_unique_filename()
        local_path = os.path.join(location, file_name_on_server)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "wb") as f:
            image.seek(0)
            f.write(image.read())
        return self.get_local_image_url(
            local_path,
            local_path.replace(settings.MEDIA_ROOT, settings.MAIN_MEDIA_URL),
        )

    def move_image(self, from_path, *new_folder):
        """Move image to new folder."""
        local_path = os.path.join(
            settings.MEDIA_ROOT, *new_folder, os.path.basename(from_path)
        )
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        shutil.move(from_path, local_path)
        return self.get_local_image_url(
            local_path, local_path.replace(settings.MEDIA_ROOT, settings.MAIN_MEDIA_URL)
        )

    def delete_image(self, image_url_dict):
        """Delete image."""
        os.remove(image_url_dict.get(ORIGIN_IMAGE).get(LOCAL_IMAGE_PATH))
        os.remove(image_url_dict.get(SEGMENTATION_IMAGE).get(LOCAL_IMAGE_PATH))
