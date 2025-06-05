# Copyright (C)
# date: 05-06-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Image Service."""

from pathlib import Path
from urllib.parse import urljoin

from django.conf import settings

from FoodCaloEstimate.estimator.constants.image_constants import (
    CLOUDINARY_PUBLIC_ID,
    CLOUDINARY_SECURE_URL,
    ORIGIN_IMAGE,
    SEGMENTATION_IMAGE,
)
from FoodCaloEstimate.estimator.services.cloudinary_service import CloudinaryService
from FoodCaloEstimate.estimator.services.food_dictionany_service import FoodDictionary
from FoodCaloEstimate.estimator.utils.generate_unique_filename import (
    generate_unique_filename,
)
from FoodCaloEstimate.queue_tasks import run_task_in_queue


class ImageService:
    """Image Service."""

    @staticmethod
    def upload_image(image_byteio, extension, *folder):
        """Upload image."""
        public_id = Path(generate_unique_filename(extension=extension)).stem
        run_task_in_queue(
            CloudinaryService().upload_image,
            image_byteio,
            public_id,
            *folder,
        )
        return {
            CLOUDINARY_SECURE_URL: urljoin(
                (
                    settings.PREFIX_PUBLIC_CLOUDINARY_URL
                    if settings.PREFIX_PUBLIC_CLOUDINARY_URL.endswith("/")
                    else settings.PREFIX_PUBLIC_CLOUDINARY_URL + "/"
                ),
                f"{public_id}.{extension}",
            ),
            CLOUDINARY_PUBLIC_ID: public_id,
        }

    @staticmethod
    def move_image(image_url, image_type, label_name):
        """Move image."""
        # image_url.update(
        #     LocalStorageService().move_image(
        #         image_url[LOCAL_IMAGE_PATH], image_type, label_name
        #     )
        # )
        CloudinaryService().move_image(
            image_url[CLOUDINARY_PUBLIC_ID], image_type, label_name
        )

    @staticmethod
    def move_image_and_update_instance(instance):
        """Move image and update instance."""
        label_name = FoodDictionary.get_name(instance.label, remove_accents=True)
        ImageService.move_image(instance.url[ORIGIN_IMAGE], ORIGIN_IMAGE, label_name)
        ImageService.move_image(
            instance.url[SEGMENTATION_IMAGE], SEGMENTATION_IMAGE, label_name
        )

        # instance.save(update_fields=["url"])

    @staticmethod
    def delete_image(image_url_dict):
        """Delete image."""
        CloudinaryService().delete_image(image_url_dict)
        # LocalStorageService().delete_image(image_url_dict)
