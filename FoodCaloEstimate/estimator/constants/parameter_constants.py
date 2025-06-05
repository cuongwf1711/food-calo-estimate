# Copyright (C)
# date: 21-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Parameter Constants."""

# FIXME: Adjust to fit the production in the future

import torch

NUM_CLASSES = 37
DTYPE_OPTIMIZE_CUDA = torch.bfloat16
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")
OPTIMIZE_AUTOCAST_PARAMETERS = {
    "dtype": DTYPE_OPTIMIZE_CUDA,
    "device_type": DEVICE.type,
}
if torch.backends.cuda.is_built() and torch.cuda.is_available():
    print("allow_tf32")
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

# Confidence Thresholds
DEFAULT_CONFIDENCE_CLASSIFICATION_THRESHOLD = 0.8

# Segmentation Model
REFERENCE_POINT = "finger"
THRESHHOLD_PIXEL_REFERENCE_POINT_AREA = 10
TEXT_PROMPT_LIST = ["food"]
TEXT_PROMPT_LIST.append(REFERENCE_POINT)
TEXT_PROMPT = ".".join(TEXT_PROMPT_LIST)

# Grounding Dino Hugging Face Model
BOX_THRESHOLD_GROUND_DINO = 0.4  # default 0.25
TEXT_THRESHOLD = 0.3  # default 0.25

# DinoX dds
BOX_THRESHOLD_DINOX = 0.3  # default 0.25
IOU_THRESHOLD = 0.7  # default 0.8
