# Copyright (C)
# date: 13-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Food segmentation model using GroundingDINO and SAM2."""

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
    OPTIMIZE_AUTOCAST_PARAMETERS,
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
    """
    Food segmentation model combining GroundingDINO for object detection and SAM2 for mask generation.

    This class performs two main tasks:
    1. Object detection: Uses GroundingDINO to detect food items in images
    2. Segmentation: Uses SAM2 to create precise masks for detected food items
    """

    @time_measure
    def __init__(self):
        """Initialize model components and load pretrained weights."""
        # Device configuration (CPU/GPU)
        self.device = DEVICE

        # Text prompts for food detection
        self.text_prompt = TEXT_PROMPT  # Single text prompt
        self.text_prompt_list = TEXT_PROMPT_LIST  # List of food categories

        # Detection thresholds
        self.box_threshold_dinox = (
            BOX_THRESHOLD_DINOX  # Confidence threshold for DINOX API
        )
        self.box_threshold_ground_dino = (
            BOX_THRESHOLD_GROUND_DINO  # Confidence threshold for GroundingDINO
        )
        self.iou_threshold = IOU_THRESHOLD  # Intersection over Union threshold for NMS
        self.text_threshold = TEXT_THRESHOLD  # Text similarity threshold

        # Image format and API configuration
        self.format_image = FORMAT_IMAGE
        self.dinox_api_path = DINOX_API_PATH
        self.dinox_model = DINOX_MODEL

        # Initialize DDS client for DINOX API (commented out)
        # self.dds_client = Client(Config(settings.API_KEY_DINOX))

        # Load GroundingDINO model for object detection
        # This model detects objects based on text descriptions
        self.processor = AutoProcessor.from_pretrained(GROUNDING_DINO_MODEL)
        self.grounding_dino_model = (
            AutoModelForZeroShotObjectDetection.from_pretrained(GROUNDING_DINO_MODEL)
            .eval()  # Set to evaluation mode
            .to(self.device)  # Move to GPU/CPU
        )

        # Load SAM2 model for segmentation
        # This model creates precise masks for detected objects
        self.SAM2_PREDICTOR = SAM2ImagePredictor(
            build_sam2(SAM2_CONFIG, SAM2_CHECKPOINT, device=self.device)  # type: ignore
        )

    @time_measure
    @torch.inference_mode()  # Disable gradient computation for inference
    @autocast(**OPTIMIZE_AUTOCAST_PARAMETERS)  # Enable mixed precision for speed
    def _get_boxes_groundino(self, image):
        """
        Detect food objects using GroundingDINO and return bounding boxes.

        Args:
            image: PIL Image object

        Returns:
            tuple: (bounding_boxes, text_labels) - detected objects with their categories
        """
        # Prepare input for the model (image + text prompts)
        inputs = self.processor(
            images=image, text=self.text_prompt_list, return_tensors="pt"
        ).to(self.device)

        # Run object detection
        results = self.processor.post_process_grounded_object_detection(
            self.grounding_dino_model(**inputs),
            inputs.input_ids,
            box_threshold=self.box_threshold_ground_dino,  # Filter low-confidence detections
            text_threshold=self.text_threshold,  # Filter poor text matches
            target_sizes=[image.size[::-1]],  # Original image dimensions
        )
        print(results)
        return results[0]["boxes"].cpu().numpy(), results[0]["text_labels"]

    @time_measure
    @torch.inference_mode()
    @autocast(**OPTIMIZE_AUTOCAST_PARAMETERS)
    def _get_masks(self, image, input_boxes, multimask_output):
        """
        Generate segmentation masks using SAM2 from detected bounding boxes.

        Args:
            image: PIL Image object
            input_boxes: Bounding boxes from object detection
            multimask_output: Whether to generate multiple mask candidates per object

        Returns:
            numpy.ndarray: Segmentation masks for detected objects
        """
        # Set the image for SAM2 predictor
        self.SAM2_PREDICTOR.set_image(np.array(image))

        # Generate masks using bounding boxes as prompts
        all_masks, _, _ = self.SAM2_PREDICTOR.predict(
            point_coords=None,  # No point prompts
            point_labels=None,  # No point labels
            box=input_boxes,  # Use bounding boxes as prompts
            multimask_output=multimask_output,  # Generate multiple mask candidates
        )

        # Clean up predictor state
        self.SAM2_PREDICTOR.reset_predictor()

        # Normalize mask dimensions for consistent processing
        return (
            all_masks
            if all_masks.ndim > 3  # Already has correct dimensions
            else (
                all_masks[np.newaxis]  # Add batch dimension
                if multimask_output
                else all_masks[:, np.newaxis, :, :]  # Add mask candidate dimension
            )
        )

    @time_measure
    @torch.inference_mode()
    def get_area_food_from_text_prompt(self, input_image):
        """
        Main method: Segment food items and calculate area per category from text prompts.

        Args:
            input_image: Input image file

        Returns:
            tuple: (overlay_image, category_areas) - annotated image and area calculations
        """
        # TODO: Optimize for production deployment

        multimask_output = True  # Generate multiple mask candidates for better quality

        # Initialize area tracking for each food category
        category_areas = {category: 0.0 for category in self.text_prompt_list}

        with Image.open(input_image).convert("RGB") as image:
            # Step 1: Detect food objects and get bounding boxes
            input_boxes, text_labels = self._get_boxes_groundino(image)

            # If no objects detected, return original image
            if len(input_boxes) == 0:
                input_image.seek(0)
                return BytesIO(input_image.read()), category_areas.values()

            # Step 2: Generate segmentation masks for detected objects
            all_masks = self._get_masks(image, input_boxes, multimask_output)

        # Step 3: Process masks and calculate areas per food category
        processed_masks = self._process_masks_and_calculate_areas(
            all_masks, text_labels, category_areas, multimask_output
        )

        # Step 4: Create visualization overlay with masks and labels
        overlay = MachineLearningService.get_overlay_image(
            image, processed_masks, text_labels
        )
        return overlay, category_areas.values()

    def _process_masks_and_calculate_areas(
        self, all_masks, text_labels, category_areas, multimask_output
    ):
        """
        Process masks and calculate pixel areas per category.

        Args:
            all_masks: Generated segmentation masks
            text_labels: Object category labels
            category_areas: Dictionary to store area calculations
            multimask_output: Whether multiple masks were generated per object

        Returns:
            list: Selected best masks for each detected object
        """
        if multimask_output:
            # Select best mask from multiple candidates based on pixel count
            all_masks_array = np.array(all_masks)

            # Calculate pixel count for each mask candidate
            mask_pixel_counts = all_masks_array.reshape(
                all_masks_array.shape[0], all_masks_array.shape[1], -1
            ).sum(axis=2)

            # Select mask with highest pixel count (largest area)
            best_mask_indices = mask_pixel_counts.argmax(axis=1)
            object_indices = np.arange(len(all_masks_array))
            pixel_counts = mask_pixel_counts[object_indices, best_mask_indices]

            # Extract selected masks
            selected_masks = all_masks_array[object_indices, best_mask_indices].astype(
                np.uint8
            )
        else:
            # Use single mask per object
            selected_masks = np.array(all_masks)[:, 0].astype(np.uint8)
            pixel_counts = selected_masks.reshape(selected_masks.shape[0], -1).sum(
                axis=1
            )

        # Group masks by food category and sum their areas
        unique_labels, inverse_indices = np.unique(
            np.array(text_labels), return_inverse=True
        )
        summed_counts = np.bincount(inverse_indices, weights=pixel_counts)

        # Update category areas with calculated pixel counts
        category_areas.update(dict(zip(unique_labels, summed_counts)))
        return list(selected_masks)

    @time_measure
    @torch.inference_mode()
    def _get_boxes_dinox(self, image):
        """
        Alternative method: Detect food objects using DINOX API and return bounding boxes.

        This is an alternative to GroundingDINO using a cloud-based API.

        Args:
            image: PIL Image object

        Returns:
            tuple: (bounding_boxes, labels) - detected objects from DINOX API
        """
        # Save image to temporary file for API upload
        with NamedTemporaryFile(suffix=f".{self.format_image}") as temp_file:
            temp_filename = temp_file.name
            image.save(temp_filename, format=self.format_image)
            infer_image_url = self.dds_client.upload_file(temp_filename)  # type: ignore

        # Create API task for object detection
        task = V2Task(
            api_path=self.dinox_api_path,
            api_body={
                "model": self.dinox_model,
                "image": infer_image_url,
                "prompt": {
                    "type": "text",
                    "text": self.text_prompt,
                },
                "targets": ["bbox"],  # Request bounding boxes
                "bbox_threshold": self.box_threshold_dinox,  # Confidence threshold
                "iou_threshold": self.iou_threshold,  # NMS threshold
            },
        )

        # Execute API request and get results
        self.dds_client.run_task(task)  # type: ignore
        print(task.result["objects"])  # type: ignore

        # Extract bounding boxes and labels from API response
        bboxes, labels = zip(
            *((obj["bbox"], obj["category"]) for obj in task.result["objects"])  # type: ignore
        )
        return np.array(bboxes), list(labels)
