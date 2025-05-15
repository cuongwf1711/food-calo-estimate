# Copyright (C)
# date: 13-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Segmentation Model."""

from io import BytesIO

import numpy as np
import torch
from PIL import Image
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from torch import autocast
from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

from FoodCaloEstimate.estimator.constants.machine_learning_constants import (
    DEVICE,
    GROUNDING_DINO_MODEL,
    REFERENCE_POINT,
    SAM2_CHECKPOINT,
    SAM2_CONFIG,
    TEXT_PROMPT,
)
from FoodCaloEstimate.estimator.services.machine_leaning_service import (
    MachineLearningService,
)


class SegmentationModel:
    """Segmentation Model."""

    def __init__(self):
        """Init."""
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

        self.processor = AutoProcessor.from_pretrained(GROUNDING_DINO_MODEL)
        self.grounding_model = AutoModelForZeroShotObjectDetection.from_pretrained(
            GROUNDING_DINO_MODEL
        ).to(DEVICE)

        self.sam2_model = build_sam2(SAM2_CONFIG, SAM2_CHECKPOINT, device=DEVICE)

    def _get_boxes(self, image):
        """Get boxes."""
        inputs = self.processor(images=image, text=TEXT_PROMPT, return_tensors="pt").to(
            DEVICE
        )
        with torch.no_grad():
            outputs = self.grounding_model(**inputs)

        results = self.processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            box_threshold=0.4,
            text_threshold=0.3,
            target_sizes=[image.size[::-1]],
        )
        return results

    def _get_masks(self, image, input_boxes):
        """Get masks."""
        with autocast(device_type=DEVICE.type, dtype=torch.bfloat16):
            sam2_predictor = SAM2ImagePredictor(self.sam2_model)
            sam2_predictor.set_image(np.array(image.convert("RGB")))
            all_masks, _, _ = sam2_predictor.predict(
                point_coords=None,
                point_labels=None,
                box=input_boxes,
                multimask_output=True,
            )
            if all_masks.ndim == 3:
                all_masks = np.expand_dims(all_masks, axis=0)

        return all_masks

    def get_area_food_from_text_prompt(self, input_image):
        """Get area food from text prompt."""
        image = Image.open(input_image)
        results = self._get_boxes(image)
        input_boxes = results[0]["boxes"].cpu().numpy()
        all_masks = self._get_masks(image, input_boxes)

        final_masks = []
        category_areas = {category: 0 for category in TEXT_PROMPT}
        text_labels = results[0]["text_labels"]
        for index, masks_per_box in enumerate(all_masks):
            mask_areas = [np.sum(mask) for mask in masks_per_box]
            largest_mask_idx = np.argmax(mask_areas)
            label = text_labels[index]
            category_areas[label] += mask_areas[largest_mask_idx]

            final_masks.append(masks_per_box[largest_mask_idx])

        overlay_image = MachineLearningService.get_overlay_image(
            image, final_masks, text_labels
        )

        return category_areas.values(), overlay_image
