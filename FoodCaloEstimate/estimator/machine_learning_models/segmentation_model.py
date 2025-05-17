# Copyright (C)
# date: 13-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Segmentation Model."""

import numpy as np
import torch
# from django.conf import settings
from PIL import Image
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from torch import autocast
from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor
# from transformers.models.auto.processing_auto import AutoProcessor
# from transformers.models.auto.modeling_auto import AutoModelForZeroShotObjectDetection

# from dds_cloudapi_sdk import Config
# from dds_cloudapi_sdk import Client
# from dds_cloudapi_sdk.tasks.v2_task import V2Task

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
        if torch.backends.cuda.is_built() and torch.cuda.is_available():
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True

        self.processor = AutoProcessor.from_pretrained(GROUNDING_DINO_MODEL)
        self.grounding_model = AutoModelForZeroShotObjectDetection.from_pretrained(
            GROUNDING_DINO_MODEL
        ).eval().to(DEVICE)

        self.sam2_model = build_sam2(SAM2_CONFIG, SAM2_CHECKPOINT, device=DEVICE)
        self.sam2_predictor = SAM2ImagePredictor(self.sam2_model)

    def _get_boxes_groundino(self, image):
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
        return results[0]["boxes"].cpu().numpy(), results[0]["text_labels"]

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
            input_boxes, text_labels = self._get_boxes_groundino(image)
            all_masks = self._get_masks(image, input_boxes)

        final_masks = []
        category_areas = {category: 0 for category in TEXT_PROMPT}
        for idx, mset in enumerate(all_masks):
            mset_sum = mset.reshape(mset.shape[0], -1).sum(axis=1)
            category_areas[text_labels[idx]] += mset_sum.max()
            final_masks.append(mset[mset_sum.argmax()].astype(np.uint8))

        overlay = MachineLearningService.get_overlay_image(image, final_masks, text_labels)
        clear_data(all_masks,final_masks)
        return overlay, category_areas.values()

    # def _get_boxes_dinox(self, image):
    #     """Get boxes use dinox."""
    #     client = Client(Config(settings))

    #     BOX_THRESHOLD = 0.2
    #     IOU_THRESHOLD = 0.8
    #     infer_image_url = client.upload_file(image)

    #     task = V2Task(
    #         api_path="/v2/task/dinox/detection",
    #         api_body={
    #             "model": "DINO-X-1.0",
    #             "image": infer_image_url,
    #             "prompt": {
    #                 "type": "text",
    #                 "text": ".".join(TEXT_PROMPT),
    #             },
    #             "targets": ["bbox", "mask"],
    #             "bbox_threshold": BOX_THRESHOLD,
    #             "iou_threshold": IOU_THRESHOLD,
    #         }
    #     )

    #     client.run_task(task)
    #     objects = task.result["objects"]


    #     input_boxes = []
    #     text_labels = []

    #     for obj in objects:
    #         input_boxes.append(obj["bbox"])
    #         text_labels.append(obj["category"])

    #     return np.array(input_boxes), text_labels
