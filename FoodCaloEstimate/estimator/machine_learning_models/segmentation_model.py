# Copyright (C)
# date: 13-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Segmentation Model."""

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
    SAM2_CHECKPOINT,
    SAM2_CONFIG,
    TEXT_PROMPT,
    TEXT_THRESHHOLD,
    BOX_THRESHHOLD,
)
from FoodCaloEstimate.estimator.services.machine_leaning_service import (
    MachineLearningService,
)

from FoodCaloEstimate.estimator.utils.clear_data import clear_data


class SegmentationModel:
    """Segmentation Model."""

    def __init__(self):
        """Init."""
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

        self.processor = AutoProcessor.from_pretrained(GROUNDING_DINO_MODEL)
        self.grounding_model = AutoModelForZeroShotObjectDetection.from_pretrained(
            GROUNDING_DINO_MODEL
        ).to(DEVICE).eval()

        self.sam2_model = build_sam2(SAM2_CONFIG, SAM2_CHECKPOINT, device=DEVICE)
        self.sam2_predictor = SAM2ImagePredictor(self.sam2_model)

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
            box_threshold=BOX_THRESHHOLD,
            text_threshold=TEXT_THRESHHOLD,
            target_sizes=[image.size[::-1]],
        )
        clear_data(inputs, outputs)
        return results

    def _get_masks(self, image, input_boxes):
        """Get masks."""
        with autocast(device_type=DEVICE.type, dtype=torch.bfloat16):
            self.sam2_predictor.set_image(np.array(image.convert("RGB")))
            all_masks, _, _ = self.sam2_predictor.predict(
                point_coords=None,
                point_labels=None,
                box=input_boxes,
                multimask_output=True,
            )
            self.sam2_predictor.reset_predictor()

        return all_masks if all_masks.ndim>3 else all_masks[np.newaxis]

    def get_area_food_from_text_prompt(self, input_image):
        """Get area food from text prompt."""
        with Image.open(input_image) as image:
            results = self._get_boxes(image)
            all_masks = self._get_masks(image, results[0]["boxes"].cpu().numpy())
            text_labels = results[0]["text_labels"]

        final_masks = []
        category_areas = {category: 0 for category in TEXT_PROMPT}
        for idx, mset in enumerate(all_masks):
            mset_sum = mset.reshape(mset.shape[0], -1).sum(axis=1)
            category_areas[text_labels[idx]] += mset_sum.max()
            final_masks.append(mset[mset_sum.argmax()].astype(np.uint8))

        overlay = MachineLearningService.get_overlay_image(image, final_masks, text_labels)
        clear_data(all_masks,final_masks)
        return overlay, category_areas.values()
