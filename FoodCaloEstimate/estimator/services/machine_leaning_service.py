# Copyright (C)
# date: 14-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Machine Learning Service."""

from io import BytesIO

import numpy as np
from PIL import Image

from FoodCaloEstimate.estimator.constants.image_constants import FORMAT_IMAGE
from FoodCaloEstimate.estimator.constants.parameter_constants import (
    TEXT_PROMPT_LIST,
    THRESHHOLD_PIXEL_REFERENCE_POINT_AREA,
)
from FoodCaloEstimate.estimator.services.food_dictionany_service import FoodDictionary


class MachineLearningService:
    """Machine Learning Service."""

    @staticmethod
    def calculate_calories(
        label: int,
        food_pixel_area: float,
        reference_point_pixel_area: float,
        REFERENCE_POINT_REAL_AREA: float,
    ) -> float:
        """Calculate calories."""
        if reference_point_pixel_area < THRESHHOLD_PIXEL_REFERENCE_POINT_AREA:
            return FoodDictionary.get_calories(label)
        return (
            food_pixel_area
            * (REFERENCE_POINT_REAL_AREA / reference_point_pixel_area)
            * (FoodDictionary.get_calories(label) / 100)
        )

    @staticmethod
    def get_overlay_image(image, masks, labels):
        """Get overlay image."""
        result_image = image.copy()
        SEGMENTATION_COLORS = {
            label: np.concatenate([np.random.random(3), [0.6]])
            for label in TEXT_PROMPT_LIST
        }
        for mask, label in zip(masks, labels):
            color_array = (np.array(SEGMENTATION_COLORS[label][:3]) * 255).astype(
                np.uint8
            )
            alpha = SEGMENTATION_COLORS[label][3]

            mask_rgb = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
            mask_rgb[mask > 0] = color_array

            mask_alpha = np.zeros((mask.shape[0], mask.shape[1]), dtype=np.uint8)
            mask_alpha[mask > 0] = int(alpha * 255)

            mask_image = Image.fromarray(mask_rgb)
            mask_alpha = Image.fromarray(mask_alpha, mode="L")
            mask_image.putalpha(mask_alpha)

            result_image.paste(mask_image, (0, 0), mask_alpha)

        buffer = BytesIO()
        result_image.save(buffer, format=FORMAT_IMAGE, quality=100)
        buffer.seek(0)
        return buffer
