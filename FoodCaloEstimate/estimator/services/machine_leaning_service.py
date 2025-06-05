# Copyright (C)
# date: 14-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Machine Learning Service."""

import os
from io import BytesIO
from pathlib import Path

import numpy as np
from django.conf import settings
from PIL import Image

from FoodCaloEstimate.estimator.constants.image_constants import (
    DEFAULT_QUALITY_IMAGE,
    FORMAT_IMAGE,
    MAX_IMAGE_SIZE,
    MIN_QUALITY_IMAGE,
    UNKNOWN_CALO,
    UNKNOWN_INDEX,
)
from FoodCaloEstimate.estimator.constants.parameter_constants import (
    TEXT_PROMPT_LIST,
    THRESHOLD_PIXEL_FOOD_AREA,
    THRESHOLD_PIXEL_REFERENCE_POINT_AREA,
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
        if label == UNKNOWN_INDEX:
            return UNKNOWN_CALO
        label_calorie = FoodDictionary.get_calories(label)
        if (
            reference_point_pixel_area < THRESHOLD_PIXEL_REFERENCE_POINT_AREA
            or food_pixel_area < THRESHOLD_PIXEL_FOOD_AREA
        ):
            return label_calorie * 100  # type: ignore
        return round(
            food_pixel_area
            * (REFERENCE_POINT_REAL_AREA / reference_point_pixel_area)
            * label_calorie,  # type: ignore
            2,
        )

    @staticmethod
    # @time_measure
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

        pil_image = Image.fromarray(img_array, mode="RGB")

        # Try saving with default quality first
        output_buffer = MachineLearningService._save_image_with_quality(
            pil_image, DEFAULT_QUALITY_IMAGE
        )
        if output_buffer.tell() <= MAX_IMAGE_SIZE:
            output_buffer.seek(0)
            return output_buffer

        # If default quality exceeds size limit, try reducing quality
        for quality in range(DEFAULT_QUALITY_IMAGE - 10, MIN_QUALITY_IMAGE - 1, -10):
            output_buffer = MachineLearningService._save_image_with_quality(
                pil_image, quality, optimize=True
            )
            if output_buffer.tell() <= MAX_IMAGE_SIZE:
                output_buffer.seek(0)
                return output_buffer

        # Fallback: convert file path to BytesIO if all attempts fail
        return MachineLearningService._convert_path_to_bytesio(
            os.path.join(settings.BASE_DIR, "images", "error.jpg")
        )

    @staticmethod
    def _save_image_with_quality(
        image: Image.Image, quality: int, optimize: bool = False
    ) -> BytesIO:
        """Save image to buffer with specified quality and return the buffer."""
        buffer = BytesIO()
        image.save(buffer, quality=quality, format=FORMAT_IMAGE, optimize=optimize)
        return buffer

    @staticmethod
    def _convert_path_to_bytesio(file_path: str) -> BytesIO:
        """Convert file path to BytesIO buffer."""
        return BytesIO(Path(file_path).read_bytes())
