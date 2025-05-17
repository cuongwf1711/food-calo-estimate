# Copyright (C)
# date: 13-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Machine Learning Constants."""

import numpy as np
import torch
from django.conf import settings


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")
DEFAULT_CONFIDENCE_THRESHOLD = 0.7

# Classification Model
ConvNextV2 = "ConvNextV2"
SwinTransformerV2 = "SwinTransformerV2"
EfficientNetV2 = "EfficientNetV2"

# Segmentation Model
REFERENCE_POINT = "finger"
REFERENCE_POINT_REAL_AREA = 1.4 * 1.8
THRESHHOLD_PIXEL_REFERENCE_POINT_AREA = 10
TEXT_PROMPT = ["food"]
TEXT_PROMPT.append(REFERENCE_POINT)
SEGMENTATION_COLORS = {
    label: np.concatenate([np.random.random(3), [0.6]]) for label in TEXT_PROMPT
}
SAM2_CHECKPOINT = rf"{settings.BASE_DIR}/FoodCaloEstimate/estimator/weights/sam2.1_hiera_large.pt"
SAM2_CONFIG = "configs/sam2.1/sam2.1_hiera_l.yaml"
GROUNDING_DINO_MODEL = "IDEA-Research/grounding-dino-tiny" # base, tiny
SegmentationModel_Key = "SegmentationModel"

BOX_THRESHHOLD=0.4
TEXT_THRESHHOLD=0.3

# Machine Learning Models
MACHINE_LEARNING_MODELS = {
    "ConvNextV2": {
        "model_name": "convnextv2_base.fcmae_ft_in22k_in1k",
        "checkpoint_path": rf"{settings.BASE_DIR}/FoodCaloEstimate/estimator/weights/convnextv2_checkpoint.pt",
    },
    "SwinTransformerV2": {
        "model_name": "swinv2_small_window16_256.ms_in1k",
        "checkpoint_path": rf"{settings.BASE_DIR}/FoodCaloEstimate/estimator/weights/swintransformerv2_checkpoint.pt",
    },
    "EfficientNetV2": {
        "model_name": "tf_efficientnetv2_s.in21k",
        "checkpoint_path": rf"{settings.BASE_DIR}/FoodCaloEstimate/estimator/weights/efficientnetv2_checkpoint.pt",
    },
}
