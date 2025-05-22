# Copyright (C)
# date: 22-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""User Profile Serializer."""

from rest_framework import serializers

from FoodCaloEstimate.iam.models.user_profile import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """User Profile Serializer."""

    auto_set_calorie_limit = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = [
            "gender",
            "age",
            "height",
            "weight",
            "calorie_limit",
            "calorie_limit_period",
            "length_reference_point",
            "width_reference_point",
            "area_reference_point",
            "length_reference_point_custom",
            "width_reference_point_custom",
            "auto_set_calorie_limit",
        ]

        extra_kwargs = {
            "length_reference_point_custom": {"write_only": True},
            "width_reference_point_custom": {"write_only": True},
        }

    def update(self, instance, validated_data):
        if validated_data.pop("auto_set_calorie_limit", False):
            validated_data["calorie_limit"] = instance.calculate_auto_calorie_limit()

        return super().update(instance, validated_data)
