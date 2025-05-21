# Copyright (C)
# date: 21-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Reference Point Serializer."""

from rest_framework import serializers

from FoodCaloEstimate.iam.models.user_profile import UserProfile


class ReferencePointSerializer(serializers.ModelSerializer):
    """Reference Point Serializer."""

    class Meta:
        """Meta class."""

        model = UserProfile
        fields = [
            "length_reference_point",
            "width_reference_point",
            "area_reference_point",
            "length_reference_point_custom",
            "width_reference_point_custom",
        ]

        extra_kwargs = {
            "length_reference_point_custom": {"write_only": True},
            "width_reference_point_custom": {"write_only": True},
        }
