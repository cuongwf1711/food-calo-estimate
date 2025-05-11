# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Change Password Serializer."""

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from FoodCaloEstimate.iam.utils.password_validator import password_validator
from FoodCaloEstimate.messages.iam_messages import (
    INCORRECT_OLD_PASSWORD,
    SAME_OLD_NEW_PASSWORD,
)


class ChangePasswordSerializer(serializers.Serializer):
    """Change Password Serializer."""

    old_password = serializers.CharField()
    new_password = serializers.CharField(
        validators=[password_validator()],
    )

    def update(self, instance, validated_data):
        """Update new password."""
        old_password = validated_data["old_password"]
        new_pasword = validated_data["new_password"]
        if instance.check_password(old_password) is False:
            raise Exception(INCORRECT_OLD_PASSWORD)
        if old_password == new_pasword:
            raise Exception(SAME_OLD_NEW_PASSWORD)
        instance.password = make_password(validated_data["new_password"])
        instance.save()
        return instance
