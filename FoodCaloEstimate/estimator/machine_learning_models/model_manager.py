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


class ModelManager:
    """Model Manager."""

    _models = {}
    _initialized = False

    @classmethod
    def initialize_models(cls):
        """Khởi tạo tất cả models"""
        if not cls._initialized:
            # ConvNextV2_Model =  ClassificationModel(
            #     MACHINE_LEARNING_MODELS[ConvNextV2]["model_name"],
            #     MACHINE_LEARNING_MODELS[ConvNextV2]["checkpoint_path"]
            # )
            EfficientNetV2_Model = ClassificationModel(
                MACHINE_LEARNING_MODELS[EfficientNetV2]["model_name"],
                MACHINE_LEARNING_MODELS[EfficientNetV2]["checkpoint_path"],
            )
            # SwinTransformerV2_Model = ClassificationModel(
            #     MACHINE_LEARNING_MODELS[SwinTransformerV2]["model_name"],
            #     MACHINE_LEARNING_MODELS[SwinTransformerV2]["checkpoint_path"]
            # )
            Segmentation_Model = SegmentationModel()
            # cls._models[ConvNextV2] = ConvNextV2_Model
            cls._models[EfficientNetV2] = EfficientNetV2_Model
            # cls._models[SwinTransformerV2] = SwinTransformerV2_Model
            cls._models[SegmentationModel_Key] = Segmentation_Model
            # Thêm các model khác nếu cần

            cls._initialized = True

    @classmethod
    def get_model(cls, model_name):
        """Get model by name."""
        if not cls._initialized:
            raise RuntimeError(
                "Models have not been initialized. Call initialize_models() first."
            )

        if model_name in cls._models:
            return cls._models[model_name]
        raise KeyError(f"Not found model: {model_name}")
