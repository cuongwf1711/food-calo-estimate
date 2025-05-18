# Copyright (C)
# date: 13-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Segmentation Model."""

from tempfile import NamedTemporaryFile

import numpy as np
import torch

# from django.conf import settings
from dds_cloudapi_sdk.tasks.v2_task import V2Task
from PIL import Image
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from torch import autocast
from transformers.models.auto.modeling_auto import AutoModelForZeroShotObjectDetection

# from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
from transformers.models.auto.processing_auto import AutoProcessor

from FoodCaloEstimate.estimator.constants.image_constants import FORMAT_IMAGE
from FoodCaloEstimate.estimator.constants.machine_learning_constants import (
    BOX_THRESHOLD,
    DEVICE,
    DINOX_API_PATH,
    DINOX_MODEL,
    GROUNDING_DINO_MODEL,
    IOU_THRESHOLD,
    SAM2_CHECKPOINT,
    SAM2_CONFIG,
    TEXT_PROMPT,
    TEXT_PROMPT_LIST,
    TEXT_THRESHOLD,
)
from FoodCaloEstimate.estimator.services.machine_leaning_service import (
    MachineLearningService,
)
from FoodCaloEstimate.estimator.utils.clear_data import clear_data
from FoodCaloEstimate.estimator.utils.custom_decorator import time_measure

# from dds_cloudapi_sdk import Config, Client
# from dds_cloudapi_sdk.tasks.v2_task import V2Task



class SegmentationModel:
    """Segmentation Model."""

    def __init__(self):
        """Init."""
        if torch.backends.cuda.is_built() and torch.cuda.is_available():
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True

        self.processor = AutoProcessor.from_pretrained(GROUNDING_DINO_MODEL)
        self.grounding_dino_model = (
            AutoModelForZeroShotObjectDetection.from_pretrained(GROUNDING_DINO_MODEL)
            .eval()
            .to(DEVICE)
        )

        # self.client = Client(Config(settings.API_KEY_DINOX))

        self.SAM2_PREDICTOR = SAM2ImagePredictor(
            build_sam2(SAM2_CONFIG, SAM2_CHECKPOINT, device=DEVICE)
        )

    @time_measure
    @torch.inference_mode()
    def _get_boxes_groundino(self, image):
        """Get boxes."""
        inputs = self.processor(
            images=image, text=TEXT_PROMPT_LIST, return_tensors="pt"
        ).to(DEVICE)
        outputs = self.grounding_dino_model(**inputs)

        results = self.processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            box_threshold=BOX_THRESHOLD,
            text_threshold=TEXT_THRESHOLD,
            target_sizes=[image.size[::-1]],
        )
        clear_data(inputs, outputs)
        return results[0]["boxes"].cpu().numpy(), results[0]["text_labels"]

    @time_measure
    @torch.inference_mode()
    def _get_masks(self, image, input_boxes, multimask_output=False):
        """Get masks."""
        with autocast(device_type=DEVICE.type, dtype=torch.bfloat16):
            self.SAM2_PREDICTOR.set_image(np.array(image.convert("RGB")))
            all_masks, _, _ = self.SAM2_PREDICTOR.predict(
                point_coords=None,
                point_labels=None,
                box=input_boxes,
                multimask_output=multimask_output,
            )
            self.SAM2_PREDICTOR.reset_predictor()

        return (
            all_masks
            if all_masks.ndim > 3
            else all_masks[np.newaxis]
            if multimask_output
            else all_masks[:, np.newaxis, :, :]
        )

    @time_measure
    @torch.inference_mode()
    def get_area_food_from_text_prompt(self, input_image):
        """Get area food from text prompt."""
        multimask_output = True
        with Image.open(input_image) as image:
            input_boxes, text_labels = self._get_boxes_groundino(image)
            all_masks = self._get_masks(image, input_boxes, multimask_output)

        final_masks = []
        category_areas = {category: 0 for category in TEXT_PROMPT_LIST}
        for idx, mset in enumerate(all_masks):
            if multimask_output:
                mset_sum = mset.reshape(mset.shape[0], -1).sum(axis=1)
                best_mask_idx = mset_sum.argmax()
                mask = mset[best_mask_idx].astype(np.uint8)
                category_areas[text_labels[idx]] += mset_sum.max()
            else:
                mask = mset[0].astype(np.uint8)
                category_areas[text_labels[idx]] += mask.sum()

            final_masks.append(mask)

        overlay = MachineLearningService.get_overlay_image(
            image, final_masks, text_labels
        )
        clear_data(all_masks, final_masks)
        return overlay, category_areas.values()

    @time_measure
    @torch.inference_mode()
    def _get_boxes_dinox(self, image):
        """Get boxes use dinox."""
        with NamedTemporaryFile(suffix=f".{FORMAT_IMAGE}") as temp_file:
            temp_filename = temp_file.name
            image.save(temp_filename, format=FORMAT_IMAGE, quality=100, optimize=True)
            infer_image_url = self.client.upload_file(temp_filename)

        task = V2Task(
            api_path=DINOX_API_PATH,
            api_body={
                "model": DINOX_MODEL,
                "image": infer_image_url,
                "prompt": {
                    "type": "text",
                    "text": TEXT_PROMPT,
                },
                "targets": ["bbox", "mask"],
                "bbox_threshold": BOX_THRESHOLD,
                "iou_threshold": IOU_THRESHOLD,
            },
        )

        self.client.run_task(task)
        bboxes, labels = zip(
            *((obj["bbox"], obj["category"]) for obj in task.result["objects"])
        )
        return np.array(bboxes), list(labels)
