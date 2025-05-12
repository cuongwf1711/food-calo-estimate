# Copyright (C)
# date: 12-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Input Image Serializer."""

from rest_framework import serializers

from FoodCaloEstimate.estimator.models.my_input_image import MyInputImage


class InputImageSerializer(serializers.ModelSerializer):
    """Input Image Serializer."""

    image_file = serializers.ImageField(write_only=True)

    class Meta:
        """Meta class."""

        model = MyInputImage
        fields = ["id", "image_file", "url", "predict", "confidence", "comment"]
        read_only_fields = ["id", "url", "predict", "confidence"]

    def validate_comment(self, value):
        if not self.instance and value:
            raise serializers.ValidationError("Comment is not allowed.")
        return value

    def create(self, validated_data):
        """Create."""
        print(type(validated_data["image_file"]))
        print(validated_data)
        return MyInputImage(
            url={
                "image_file": "test",
            },
            label=-1,
            predict=-1,
            confidence=0.0,
            user=self.context["request"].user,
            staff=None,
            calo=0.0,
        )

    def update(self, instance, validated_data):
        """Update."""
        print(instance)
        print(validated_data)
        return True
