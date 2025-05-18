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
            cls._force_cleanup()

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

    @classmethod
    def release_models(cls):
        """Release all models."""
        if cls._initialized:
            cls._force_cleanup()
            del cls._models
            del cls._initialized

    @classmethod
    def _force_cleanup(cls):
        """Force cleanup of all models."""
        for my_model in cls._models.values():
            if hasattr(my_model, 'model'):
                del my_model.model
            if hasattr(my_model, 'sam2_predictor'):
                my_model.sam2_predictor.reset_predictor()
                del my_model.sam2_predictor
            del my_model

        clear_data()
