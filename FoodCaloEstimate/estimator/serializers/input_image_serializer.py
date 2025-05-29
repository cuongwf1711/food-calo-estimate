# Copyright (C)
# date: 12-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Input Image Serializer."""


from rest_framework import serializers

from FoodCaloEstimate.estimator.constants.image_constants import (
    DEFAULT_URL,
    MAX_IMAGE_SIZE,
    ORIGIN_IMAGE,
    SEGMENTATION_IMAGE,
    UNKNOWN,
)
from FoodCaloEstimate.estimator.constants.model_checkpoint_constants import (
    SegmentationModel_Key,
)
from FoodCaloEstimate.estimator.machine_learning_models.model_manager import (
    ModelManager,
)
from FoodCaloEstimate.estimator.models.my_input_image import MyInputImage
from FoodCaloEstimate.estimator.services.food_dictionany_service import FoodDictionary
from FoodCaloEstimate.estimator.services.image_service import ImageService
from FoodCaloEstimate.estimator.services.machine_leaning_service import (
    MachineLearningService,
)
from FoodCaloEstimate.queue_tasks import run_parallel_tasks_in_queue


class InputImageSerializer(serializers.ModelSerializer):
    """Input Image Serializer."""

    image_file = serializers.ImageField(write_only=True)
    public_url = serializers.SerializerMethodField()
    predict_name = serializers.SerializerMethodField()

    def get_public_url(self, obj):
        """Get public url."""
        return {
            image_type: obj.url[image_type][DEFAULT_URL]
            for image_type in (ORIGIN_IMAGE, SEGMENTATION_IMAGE)
        }

    def get_predict_name(self, obj):
        """Get predict name."""
        return FoodDictionary.get_name(obj.predict)

    class Meta:
        """Meta class."""

        model = MyInputImage
        fields = [
            "id",
            "predict",
            "confidence_percentage",
            "created_at",
            "public_url",
            "predict_name",
            "comment",
            "image_file",
            "calo",
        ]
        read_only_fields = [
            "id",
            "predict",
            "confidence_percentage",
            "created_at",
        ]
        extra_kwargs = {
            "calo": {
                "required": False,
            }
        }

    # def validate_comment(self, value):
    #     """Validate comment field."""
    #     already_comment = self.instance and self.instance.comment
    #     if already_comment:
    #         raise serializers.ValidationError("Comment is not allowed.")
    #     return value

    def validate_image_file(self, image):
        """Validate method."""
        if image.size > MAX_IMAGE_SIZE:
            raise serializers.ValidationError(
                f"Image size must less than {MAX_IMAGE_SIZE // 1024 // 1024} mb."
            )
        return image

    def create(self, validated_data):
        """Create."""

        validated_data.clear()
        validated_data["user"] = self.context["request"].user
        validated_data["confidence"], validated_data["predict"] = 1, 1
        validated_data["calo"] = 100
        validated_data["url"] = {
            ORIGIN_IMAGE: {
                DEFAULT_URL: "https://res.cloudinary.com/dp18ugn5e/image/upload/v1748492126/rmd9vc5jdskfmtxdcepb.jpg",
            },
            SEGMENTATION_IMAGE: {
                DEFAULT_URL: "https://res.cloudinary.com/dp18ugn5e/image/upload/v1748492126/pbuvf0trfohfs25du5kn.jpg",
            },
        }
        return super().create(validated_data)

        image_file = validated_data["image_file"]
        validated_data.clear()

        (
            validated_data["confidence"],
            validated_data["predict"],
        ) = ModelManager.get_model().predict(image_file)

        segmentation_image_byteio, (
            food_pixel_area,
            reference_point_pixel_area,
        ) = ModelManager.get_model(
            SegmentationModel_Key
        ).get_area_food_from_text_prompt(
            image_file
        )

        image_file.seek(0)
        user = self.context["request"].user
        (
            origin_image_cloudinary,
            segmentation_image_cloudinary,
            validated_data["calo"],
        ) = run_parallel_tasks_in_queue(
            (ImageService.upload_image, (image_file.read(), ORIGIN_IMAGE, UNKNOWN), {}),
            (
                ImageService.upload_image,
                (segmentation_image_byteio, SEGMENTATION_IMAGE, UNKNOWN),
                {},
            ),
            (
                MachineLearningService.calculate_calories,
                (
                    validated_data["predict"],
                    food_pixel_area,
                    reference_point_pixel_area,
                    user.userprofile.area_reference_point,
                ),
                {},
            ),
        )
        segmentation_image_byteio.close()

        validated_data["url"] = {
            ORIGIN_IMAGE: origin_image_cloudinary,
            SEGMENTATION_IMAGE: segmentation_image_cloudinary,
        }
        validated_data["user"] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update."""
        comment = validated_data.get("comment")
        calo = validated_data.get("calo")
        if comment or calo:
            validated_data.clear()
            if comment:
                validated_data["comment"] = comment
            if calo:
                validated_data["calo"] = calo
            return super().update(instance, validated_data)
        return instance


def test1(a, b, c):
    """Test function."""
    print(a, b, c)
    return a + b + c


# run_parallel_tasks_in_queue(
#     (test1, (1, 2, 3), {}),
#     (test1, (4, 5, 6), {})
# )
# return True
