# Copyright (C)
# date: 14-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Cloudinary Service."""

import os

import cloudinary
import cloudinary.api
import cloudinary.uploader
from django.conf import settings

from FoodCaloEstimate.estimator.constants.image_constants import (
    CLOUDINARY_PUBLIC_ID,
    CLOUDINARY_SECURE_URL,
    ORIGIN_IMAGE,
    SEGMENTATION_IMAGE,
)
from FoodCaloEstimate.estimator.utils.custom_decorator import time_measure


class CloudinaryService:
    """Cloudinary service class."""

    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )

    @time_measure
    def upload_image(self, image, public_id, *folder):
        """Upload image to folder."""
        asset_folder = os.path.join(*folder)
        response = cloudinary.uploader.upload(
            file=image,
            public_id=public_id,
            asset_folder=asset_folder,
        )
        return {
            CLOUDINARY_SECURE_URL: response[CLOUDINARY_SECURE_URL],
            CLOUDINARY_PUBLIC_ID: response[CLOUDINARY_PUBLIC_ID],
        }

    def move_image(self, public_id, *new_folder):
        """Move image to folder."""
        return cloudinary.api.update(
            public_id,
            asset_folder=os.path.join(*new_folder),
        )

    def delete_image(self, image_dict):
        """Delete image."""
        cloudinary.api.delete_resources(
            image_dict.get(ORIGIN_IMAGE).get(CLOUDINARY_PUBLIC_ID)
        )
        cloudinary.api.delete_resources(
            image_dict.get(SEGMENTATION_IMAGE).get(CLOUDINARY_PUBLIC_ID)
        )

    def init_folder(self, path):
        """Initialize the folder."""
        cloudinary.api.create_folder(path)
