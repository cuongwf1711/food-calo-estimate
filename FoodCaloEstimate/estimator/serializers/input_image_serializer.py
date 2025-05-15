# Copyright (C)
# date: 12-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Input Image Serializer."""

import io
import os
import time

from rest_framework import serializers

from FoodCaloEstimate.estimator.constants.image_constants import (
    CLOUDINARY_PATH,
    CLOUDINARY_SECURE_URL,
    LOCAL_IMAGE_URL,
    LOCAL_PATH,
    MAX_IMAGE_SIZE,
    ORIGIN_IMAGE,
    SEGMENTATION_IMAGE,
)
from FoodCaloEstimate.estimator.constants.machine_learning_constants import (
    EfficientNetV2,
    SegmentationModel_Key,
)
from FoodCaloEstimate.estimator.machine_learning_models.model_manager import (
    ModelManager,
)
from FoodCaloEstimate.estimator.models.my_input_image import MyInputImage
from FoodCaloEstimate.estimator.services.cloudinary_service import CloudinaryService
from FoodCaloEstimate.estimator.services.food_dictionany_service import FoodDictionary
from FoodCaloEstimate.estimator.services.local_storage_service import (
    LocalStorageService,
)
from FoodCaloEstimate.estimator.services.machine_leaning_service import (
    MachineLearningService,
)
from FoodCaloEstimate.queue_tasks import run_parallel_tasks_in_queue


class InputImageSerializer(serializers.ModelSerializer):
    """Input Image Serializer."""

    image_file = serializers.ImageField(write_only=True)
    public_url = serializers.SerializerMethodField()
    predict_text = serializers.SerializerMethodField()

    def get_public_url(self, obj):
        """Get public url."""
        return {
            ORIGIN_IMAGE: obj.url[ORIGIN_IMAGE][LOCAL_IMAGE_URL],
            SEGMENTATION_IMAGE: obj.url[SEGMENTATION_IMAGE][LOCAL_IMAGE_URL],
        }

    def get_predict_text(self, obj):
        """Get predict text."""
        return FoodDictionary.get_name(obj.predict)

    class Meta:
        """Meta class."""

        model = MyInputImage
        fields = [
            "id",
            "image_file",
            "predict",
            "confidence",
            "comment",
            # "calo",
            "public_url",
            "predict_text",
            "created_at",
        ]
        read_only_fields = ["id", "predict", "confidence", "created_at"]
        # extra_kwargs = {
        #     "calo": {"required": False},
        # }

    def validate_comment(self, value):
        already_comment = self.instance and self.instance.comment
        if already_comment:
            raise serializers.ValidationError("Comment is not allowed.")
        return value

    # def validate_calo(self, value):
    #     """Validate calo."""
    #     already_comment = self.instance and self.instance.comment
    #     if already_comment:
    #         raise serializers.ValidationError("Calo is not allowed.")
    #     return value

    def validate_image_file(self, image):
        """Validate method."""
        if image.size > MAX_IMAGE_SIZE:
            raise serializers.ValidationError(
                "Image size must less than {SIZE} mb.".format(
                    SIZE=MAX_IMAGE_SIZE // 1024 // 1024
                )
            )
        return image

    def create(self, validated_data):
        """Create."""
        image_file = validated_data.pop("image_file")
        validated_data.clear()

        validated_data["confidence"], validated_data["predict"] = ModelManager.get_model(
            EfficientNetV2
        ).predict(image_file)
        (food_pixel_area, reference_point_pixel_area), byteio = ModelManager.get_model(
            SegmentationModel_Key
        ).get_area_food_from_text_prompt(image_file)

        image_file.seek(0)
        image_byteio = io.BytesIO(image_file.read())

        origin_image_cloudinary, \
        origin_image_local, \
        segmentation_image_cloudinary, \
        segmentation_image_local, \
        validated_data["calo"] = run_parallel_tasks_in_queue(
            (
                CloudinaryService().upload_image,
                (image_byteio, ORIGIN_IMAGE),
                {}
            ),
            (
                LocalStorageService().upload_image,
                (image_byteio, ORIGIN_IMAGE),
                {}
            ),
            (CloudinaryService().upload_image, (byteio, SEGMENTATION_IMAGE), {}),
            (LocalStorageService().upload_image, (byteio, SEGMENTATION_IMAGE), {}),
            (
                MachineLearningService.calculate_calories,
                (validated_data["predict"], food_pixel_area, reference_point_pixel_area),
                {}
            ),
        )

        validated_data["url"] = {
            ORIGIN_IMAGE: {
                **origin_image_cloudinary,
                **origin_image_local,
            },
            SEGMENTATION_IMAGE: {
                **segmentation_image_cloudinary,
                **segmentation_image_local,
            },
        }
        validated_data["user"] = self.context["request"].user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update."""
        comment = validated_data.pop("comment", None)
        validated_data.clear()
        if comment:
            validated_data["comment"] = comment
        return super().update(instance, validated_data)


def test1(a, b, c):
    """Test function."""
    print(a, b, c)
    return a + b + c


# run_parallel_tasks_in_queue(
#     (test1, (1, 2, 3), {}),
#     (test1, (4, 5, 6), {})
# )
# return True


# image_byteio = io.BytesIO(image_file.read())
# image_file = image_byteio

# origin_image_cloudinary, \
# origin_image_local, \
# (confidence, label), \
# ((food_pixel_area, reference_point_pixel_area), byteio) = run_parallel_tasks_in_queue(
#     (CloudinaryService().upload_image, (image_file, ORIGIN_IMAGE), {}),
#     (LocalStorageService().upload_image, (image_file, ORIGIN_IMAGE), {}),
#     (ModelManager.get_model(EfficientNetV2).predict, (image_file,), {}),
#     (ModelManager.get_model(SegmentationModel_Key).get_area_food_from_text_prompt, (image_file,), {}),
# )
