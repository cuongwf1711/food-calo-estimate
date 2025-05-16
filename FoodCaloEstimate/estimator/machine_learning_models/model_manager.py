# Copyright (C)
# date: 14-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Model Manager."""

from FoodCaloEstimate.estimator.constants.machine_learning_constants import (
    MACHINE_LEARNING_MODELS,
    ConvNextV2,
    EfficientNetV2,
    SegmentationModel_Key,
    SwinTransformerV2,
)
from FoodCaloEstimate.estimator.machine_learning_models.classification_model import (
    ClassificationModel,
)
from FoodCaloEstimate.estimator.machine_learning_models.segmentation_model import (
    SegmentationModel,
)
from FoodCaloEstimate.estimator.utils.clear_data import clear_data



class ModelManager:
    """Model Manager."""

    _models = {}
    _initialized = False

    @classmethod
    def initialize_models(cls):
        """Khởi tạo tất cả models"""
        if not cls._initialized:
            clear_data()
            models = [EfficientNetV2] # , ConvNextV2, SwinTransformerV2
            for model in models:
                cls._models[model] = ClassificationModel(
                    MACHINE_LEARNING_MODELS[model]["model_name"],
                    MACHINE_LEARNING_MODELS[model]["checkpoint_path"],
                )

            cls._models[SegmentationModel_Key] = SegmentationModel()

            cls._initialized = True

    @classmethod
    def get_model(cls, model_name=None):
        """Get model by name."""
        if not cls._initialized:
            raise RuntimeError(
                "Models have not been initialized. Call initialize_models() first."
            )

        return cls._models.get(model_name, cls._models[EfficientNetV2])
