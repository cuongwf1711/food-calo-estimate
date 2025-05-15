# Copyright (C)
# date: 13-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Classification Model."""

import timm
import torch
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

from FoodCaloEstimate.estimator.constants.machine_learning_constants import (
    DEFAULT_CONFIDENCE_THRESHOLD,
    DEVICE,
)
from FoodCaloEstimate.estimator.constants.my_food_calo_estimate_constants import (
    NUM_CLASSES,
)


class ClassificationModel:
    """Classification Model."""

    def __init__(self, model_name: str, checkpoint_path: str) -> None:
        """Init."""
        self.model = timm.create_model(
            model_name, pretrained=False, num_classes=NUM_CLASSES
        )

        self.model.load_state_dict(
            torch.load(checkpoint_path, weights_only=True, map_location=DEVICE)
        )

        self.model = self.model.to(DEVICE).eval()

        data_config = timm.data.resolve_model_data_config(self.model)

        self.train_transforms = timm.data.create_transform(
            **data_config, is_training=True
        )
        self.val_transforms = timm.data.create_transform(
            **data_config, is_training=False
        )

    @torch.no_grad()
    def predict(
        self,
        input_image: InMemoryUploadedFile,
        confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
    ) -> int:
        """Predict."""
        # Preprocess the input image
        tensor_batch = (
            self.val_transforms(Image.open(input_image).convert("RGB"))
            .unsqueeze(0)
            .to(DEVICE)
        )

        # Forward pass
        raw_logits = self.model(tensor_batch)
        probabilities = torch.softmax(raw_logits, dim=1)

        # Get the predicted class index and confidence score
        confidence_score, predicted_idx = probabilities.max(dim=1)
        conf = confidence_score.item()
        idx = predicted_idx.item()

        if conf < confidence_threshold:
            return 1 - conf, -1
        return conf, idx
