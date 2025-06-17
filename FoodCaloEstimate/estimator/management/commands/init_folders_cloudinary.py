# Copyright (C)
# date: 16-06-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Init Folder Cloudinary Command."""

import os

from django.core.management.base import BaseCommand

from FoodCaloEstimate.estimator.constants.image_constants import (
    ORIGIN_IMAGE,
    SEGMENTATION_IMAGE,
)
from FoodCaloEstimate.estimator.services.cloudinary_service import CloudinaryService
from FoodCaloEstimate.estimator.services.food_dictionany_service import FoodDictionary


class Command(BaseCommand):  # init_folders_cloudinary
    """Command."""

    def handle(self, *args, **kwargs):
        """Handle."""
        main_folders = [ORIGIN_IMAGE, SEGMENTATION_IMAGE]
        for folder in main_folders:
            for food_name_no_accent in FoodDictionary.id_to_food.values():
                try:
                    t = os.path.join(folder, food_name_no_accent["name_no_accent"])
                    print(t)
                    CloudinaryService().init_folder(t)
                except Exception as e:
                    print(e)
                    continue
        self.stdout.write(self.style.SUCCESS("Successfully"))
