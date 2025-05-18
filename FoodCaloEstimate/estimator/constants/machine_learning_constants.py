# Copyright (C)
# date: 13-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Machine Learning Constants."""

import os

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
TEXT_PROMPT_LIST = ["food"]
TEXT_PROMPT_LIST.append(REFERENCE_POINT)
TEXT_PROMPT = ".".join(TEXT_PROMPT_LIST)

FOLDER_WEIGHT = os.path.join(
    settings.BASE_DIR, "FoodCaloEstimate", "estimator", "weights"
)

SAM2_VERSION = "sam2.1_hiera_t"
SAM2_CHECKPOINT = os.path.join(FOLDER_WEIGHT, f"{SAM2_VERSION}.pt")
SAM2_CONFIG = f"configs/sam2.1/{SAM2_VERSION}.yaml"
GROUNDING_DINO_MODEL = "IDEA-Research/grounding-dino-tiny"  # base, tiny
DINOX_API_PATH = "/v2/task/dinox/detection"
DINOX_MODEL = "DINO-X-1.0"
SegmentationModel_Key = "SegmentationModel"

BOX_THRESHOLD = 0.4  # default both 0.25
TEXT_THRESHOLD = 0.3  # default 0.25
IOU_THRESHOLD = 0.8  # default 0.8

# Machine Learning Models
MACHINE_LEARNING_MODELS = {
    "ConvNextV2": {
        "model_name": "convnextv2_base.fcmae_ft_in22k_in1k",
        "checkpoint_path": os.path.join(FOLDER_WEIGHT, "convnextv2_checkpoint.pt"),
    },
    "SwinTransformerV2": {
        "model_name": "swinv2_small_window16_256.ms_in1k",
        "checkpoint_path": os.path.join(
            FOLDER_WEIGHT, "swintransformerv2_checkpoint.pt"
        ),
    },
    "EfficientNetV2": {
        "model_name": "tf_efficientnetv2_s.in21k",
        "checkpoint_path": os.path.join(FOLDER_WEIGHT, "efficientnetv2_checkpoint.pt"),
    },
}
