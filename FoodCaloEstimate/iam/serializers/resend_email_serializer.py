# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Resend Email Serializer."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from FoodCaloEstimate.iam.constants.django_model_constant import MAX_LENGTH_CHAR_FIELD
from FoodCaloEstimate.iam.utils.otp_utils import set_otp_to_redis_or_raise_exception
from FoodCaloEstimate.iam.utils.send_email_signup import send_email_signup
from FoodCaloEstimate.iam.utils.user_utils import get_valid_user_or_raise_exeption

User = get_user_model()


class ResendEmailSerializer(serializers.Serializer):
    """Resend Email Serializer."""

    email = serializers.EmailField(max_length=MAX_LENGTH_CHAR_FIELD)

    def validate(self, attrs):
        """Validate."""
        email = attrs["email"]
        get_valid_user_or_raise_exeption(email)
        attrs["otp"] = set_otp_to_redis_or_raise_exception(email)
        return super().validate(attrs)

    def create(self, validated_data):
        """Create."""
        send_email_signup(
            validated_data["email"],
            validated_data["otp"],
        )
        return True
