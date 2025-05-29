# Copyright (C)
# date: 13-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Machine Learning Constants."""

import os

from django.conf import settings

# Classification Model
ConvNextV2 = "ConvNextV2"
SwinTransformerV2 = "SwinTransformerV2"
EfficientNetV2 = "EfficientNetV2"

FOLDER_WEIGHT = os.path.join(
    settings.BASE_DIR, "FoodCaloEstimate", "estimator", "weights"
)

# FIXME: Ensure the weights folder exists, adjust to fit hardware
SAM2_VERSION = "sam2.1_hiera_l"
SAM2_CHECKPOINT = os.path.join(FOLDER_WEIGHT, f"{SAM2_VERSION}.pt")
SAM2_CONFIG = f"configs/sam2.1/{SAM2_VERSION}.yaml"
GROUNDING_DINO_MODEL = "IDEA-Research/grounding-dino-tiny"  # base, tiny
DINOX_API_PATH = "/v2/task/grounding_dino/detection"  # /v2/task/grounding_dino/detection, /v2/task/dinox/detection
DINOX_MODEL = "GroundingDino-1.6-Pro"  # GroundingDino-1.6-Pro, DINO-X-1.0
SegmentationModel_Key = "SegmentationModel"

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
