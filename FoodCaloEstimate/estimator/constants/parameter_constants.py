# Copyright (C)
# date: 21-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Parameter Constants."""

# FIXME: Adjust to fit the production in the future

import torch

NUM_CLASSES = 37
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")
DEFAULT_CONFIDENCE_THRESHOLD = 0.7

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
