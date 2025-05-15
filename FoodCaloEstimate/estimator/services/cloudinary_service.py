# Copyright (C)
# date: 14-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Cloudinary Service."""

import os

import cloudinary
import cloudinary.uploader
from django.conf import settings

from FoodCaloEstimate.estimator.constants.image_constants import (
    CLOUDINARY_PATH,
    CLOUDINARY_PUBLIC_ID,
    CLOUDINARY_SECURE_URL,
    ORIGIN_IMAGE,
    SEGMENTATION_IMAGE,
)


class CloudinaryService:
    """Cloudinary service class."""

    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )

    def upload_image(self, image, *folder):
        """Upload image to folder."""
        asset_folder = os.path.join(*folder)
        response = cloudinary.uploader.upload(
            file=image,
            asset_folder=asset_folder,
        )
        return {
            CLOUDINARY_SECURE_URL: response[CLOUDINARY_SECURE_URL],
            CLOUDINARY_PUBLIC_ID: response[CLOUDINARY_PUBLIC_ID],
        }
