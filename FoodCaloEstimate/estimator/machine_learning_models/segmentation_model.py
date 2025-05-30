# Copyright (C)
# date: 13-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Segmentation Model."""

from io import BytesIO
from tempfile import NamedTemporaryFile

import numpy as np
import torch

# from dds_cloudapi_sdk import Client, Config
from dds_cloudapi_sdk.tasks.v2_task import V2Task

# from django.conf import settings
from PIL import Image
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from torch import autocast
from transformers.models.auto.modeling_auto import AutoModelForZeroShotObjectDetection

# from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
from transformers.models.auto.processing_auto import AutoProcessor

from FoodCaloEstimate.estimator.constants.image_constants import FORMAT_IMAGE
from FoodCaloEstimate.estimator.constants.model_checkpoint_constants import (
    DINOX_API_PATH,
    DINOX_MODEL,
    GROUNDING_DINO_MODEL,
    SAM2_CHECKPOINT,
    SAM2_CONFIG,
)
from FoodCaloEstimate.estimator.constants.parameter_constants import (
    BOX_THRESHOLD_DINOX,
    BOX_THRESHOLD_GROUND_DINO,
    DEVICE,
    IOU_THRESHOLD,
    TEXT_PROMPT,
    TEXT_PROMPT_LIST,
    TEXT_THRESHOLD,
)
from FoodCaloEstimate.estimator.services.machine_leaning_service import (
    MachineLearningService,
)
from FoodCaloEstimate.estimator.utils.custom_decorator import time_measure

# from FoodCaloEstimate.estimator.utils.run_try__loop_funcs import run_try_loop_funcs


class SegmentationModel:
    """Segmentation Model."""

    @time_measure
    def __init__(self):
        """Init."""
        # Constants
        self.device = DEVICE
        self.text_prompt = TEXT_PROMPT
        self.text_prompt_list = TEXT_PROMPT_LIST
        self.box_threshold_dinox = BOX_THRESHOLD_DINOX
        self.box_threshold_ground_dino = BOX_THRESHOLD_GROUND_DINO
        self.iou_threshold = IOU_THRESHOLD
        self.text_threshold = TEXT_THRESHOLD
        self.format_image = FORMAT_IMAGE
        self.dinox_api_path = DINOX_API_PATH
        self.dinox_model = DINOX_MODEL
        self.dtype_optimize_cuda = torch.bfloat16
        # self.dds_client = Client(Config(settings.API_KEY_DINOX))

        if torch.backends.cuda.is_built() and torch.cuda.is_available():
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True

        self.processor = AutoProcessor.from_pretrained(GROUNDING_DINO_MODEL)
        self.grounding_dino_model = (
            AutoModelForZeroShotObjectDetection.from_pretrained(GROUNDING_DINO_MODEL)
            .eval()
            .to(self.device)
        )

        self.SAM2_PREDICTOR = SAM2ImagePredictor(
            build_sam2(SAM2_CONFIG, SAM2_CHECKPOINT, device=self.device)  # type: ignore
        )

    @time_measure
    @torch.inference_mode()
    def _get_boxes_groundino(self, image):
        """Get boxes."""
        with autocast(device_type=self.device.type, dtype=self.dtype_optimize_cuda):
            inputs = self.processor(
                images=image, text=self.text_prompt_list, return_tensors="pt"
            ).to(self.device)

            results = self.processor.post_process_grounded_object_detection(
                self.grounding_dino_model(**inputs),
                inputs.input_ids,
                box_threshold=self.box_threshold_ground_dino,
                text_threshold=self.text_threshold,
                target_sizes=[image.size[::-1]],
            )
            print(results)
            return results[0]["boxes"].cpu().numpy(), results[0]["text_labels"]

    @time_measure
    @torch.inference_mode()
    def _get_masks(self, image, input_boxes, multimask_output=False):
        """Get masks."""
        with autocast(device_type=self.device.type, dtype=self.dtype_optimize_cuda):
            self.SAM2_PREDICTOR.set_image(np.array(image))
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
            else (
                all_masks[np.newaxis]
                if multimask_output
                else all_masks[:, np.newaxis, :, :]
            )
        )

    @time_measure
    @torch.inference_mode()
    def get_area_food_from_text_prompt(self, input_image):
        """Get area food from text prompt."""
        # FIXME: Adjust to fit the production in the future

        multimask_output = True
        category_areas = {category: 0.0 for category in self.text_prompt_list}
        with Image.open(input_image).convert("RGB") as image:
            input_boxes, text_labels = self._get_boxes_groundino(image)

            if len(input_boxes) == 0:
                input_image.seek(0)
                return BytesIO(input_image.read()), category_areas.values()
            # input_boxes, text_labels = run_try_loop_funcs(
            #     [self._get_boxes_dinox, self._get_boxes_groundino], image
            # )
            all_masks = self._get_masks(image, input_boxes, multimask_output)

        final_masks = []
        for idx, mset in enumerate(all_masks):
            if multimask_output:
                mset_sum = mset.reshape(mset.shape[0], -1).sum(axis=1)
                best_mask_idx = mset_sum.argmax()
                mask = mset[best_mask_idx].astype(np.uint8)
                category_areas[text_labels[idx]] += float(mset_sum.max())
            else:
                mask = mset[0].astype(np.uint8)
                category_areas[text_labels[idx]] += float(mask.sum())

            final_masks.append(mask)

        overlay = MachineLearningService.get_overlay_image(
            image, final_masks, text_labels
        )
        return overlay, category_areas.values()

    @time_measure
    @torch.inference_mode()
    def _get_boxes_dinox(self, image):
        """Get boxes use dinox."""
        with NamedTemporaryFile(suffix=f".{self.format_image}") as temp_file:
            temp_filename = temp_file.name
            image.save(
                temp_filename, format=self.format_image, quality=100, optimize=True
            )
            infer_image_url = self.dds_client.upload_file(temp_filename)  # type: ignore

        task = V2Task(
            api_path=self.dinox_api_path,
            api_body={
                "model": self.dinox_model,
                "image": infer_image_url,
                "prompt": {
                    "type": "text",
                    "text": self.text_prompt,
                },
                "targets": ["bbox"],
                "bbox_threshold": self.box_threshold_dinox,
                "iou_threshold": self.iou_threshold,
            },
        )

        self.dds_client.run_task(task)  # type: ignore
        print(task.result["objects"])  # type: ignore
        bboxes, labels = zip(
            *((obj["bbox"], obj["category"]) for obj in task.result["objects"])  # type: ignore
        )
        return np.array(bboxes), list(labels)
