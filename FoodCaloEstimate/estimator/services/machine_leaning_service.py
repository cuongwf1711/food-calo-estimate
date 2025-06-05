# Copyright (C)
# date: 14-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Machine Learning Service."""

from io import BytesIO

import numpy as np
from PIL import Image

from FoodCaloEstimate.estimator.constants.image_constants import (
    FORMAT_IMAGE,
    UNKNOWN_CALO,
    UNKNOWN_INDEX,
)
from FoodCaloEstimate.estimator.constants.parameter_constants import (
    TEXT_PROMPT_LIST,
    THRESHHOLD_PIXEL_REFERENCE_POINT_AREA,
)
from FoodCaloEstimate.estimator.services.food_dictionany_service import FoodDictionary
from FoodCaloEstimate.estimator.utils.custom_decorator import time_measure


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
        if label == UNKNOWN_INDEX:
            return UNKNOWN_CALO
        label_calorie = FoodDictionary.get_calories(label)
        if reference_point_pixel_area < THRESHHOLD_PIXEL_REFERENCE_POINT_AREA:
            return label_calorie * 100  # type: ignore
        return round(
            food_pixel_area
            * (REFERENCE_POINT_REAL_AREA / reference_point_pixel_area)
            * label_calorie,  # type: ignore
            2,
        )

    @staticmethod
    @time_measure
    def get_overlay_image(image, masks, labels):
        """Get overlay image."""
        SEGMENTATION_COLORS = {
            label: np.concatenate([np.random.random(3), [0.6]])
            for label in TEXT_PROMPT_LIST
        }
        img_array = np.array(image, dtype=np.uint8)
        for mask, label in zip(masks, labels):
            # Use boolean indexing for faster mask application
            mask_bool = mask.astype(bool) if mask.dtype != bool else mask
            if not mask_bool.any():
                continue

            color_info = SEGMENTATION_COLORS[label]
            color_rgb = (color_info[:3] * 255).astype(np.uint8)
            alpha = color_info[3]

            img_array[mask_bool] = (
                img_array[mask_bool].astype(np.float32) * (1 - alpha)
                + color_rgb.astype(np.float32) * alpha
            ).astype(np.uint8)

        buffer = BytesIO()
        Image.fromarray(img_array, mode="RGB").save(buffer, format=FORMAT_IMAGE)
        buffer.seek(0)
        return buffer
