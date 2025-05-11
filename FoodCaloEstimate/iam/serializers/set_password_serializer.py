# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Set Password Serializer."""

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from FoodCaloEstimate.iam.constants.auth_constants import OTP_DB_REDIS
from FoodCaloEstimate.iam.constants.django_model_constant import MAX_LENGTH_CHAR_FIELD
from FoodCaloEstimate.iam.services.redis_services import RedisService
from FoodCaloEstimate.iam.utils.otp_utils import (
    check_valid_client_otp_or_raise_exception,
)
from FoodCaloEstimate.iam.utils.password_validator import password_validator
from FoodCaloEstimate.messages.iam_messages import (
    EXISTED_ACOUNT,
    OTP_EXPIRED,
    OTP_INVALID,
)

User = get_user_model()


class SetPasswordSerializer(serializers.Serializer):
    """Set Password Serializer."""

    email = serializers.EmailField(max_length=MAX_LENGTH_CHAR_FIELD)
    otp = serializers.CharField()
    password = serializers.CharField(
        validators=[password_validator()],
    )

    def validate(self, attrs):
        """Validate email and token data."""
        email = attrs["email"]
        try:
            if User.objects.get(username=email):
                raise serializers.ValidationError(EXISTED_ACOUNT)
        except User.DoesNotExist:
            check_valid_client_otp_or_raise_exception(email, attrs["otp"])
        return attrs

    def create(self, validated_data):
        """Create."""
        return User.objects.create(
            username=validated_data["email"],
            password=make_password(validated_data["password"]),
        )
