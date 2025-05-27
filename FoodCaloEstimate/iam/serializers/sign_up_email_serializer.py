# Copyright (C)
# date: 09-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Sign Up Serializer."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from FoodCaloEstimate.iam.constants.django_model_constant import MAX_LENGTH_CHAR_FIELD
from FoodCaloEstimate.iam.utils.otp_utils import set_otp_to_redis_or_raise_exception
from FoodCaloEstimate.iam.utils.send_email_signup import send_email_signup
from FoodCaloEstimate.messages.iam_messages import EXISTED_ACOUNT

User = get_user_model()


class SignupEmailSerializer(serializers.Serializer):
    """Sign Up Serializer."""

    email = serializers.EmailField(max_length=MAX_LENGTH_CHAR_FIELD)

    def validate(self, attrs):
        """Validate."""
        email = attrs["email"]

        try:
            if User.objects.get(username=email):
                print("Existed account")
                raise serializers.ValidationError(EXISTED_ACOUNT)
        except User.DoesNotExist:
            print("Not existed account")
            attrs["otp"] = set_otp_to_redis_or_raise_exception(email)
        return super().validate(attrs)

    def create(self, validated_data):
        """Create."""
        send_email_signup(
            validated_data["email"],
            validated_data["otp"],
        )
        return True
