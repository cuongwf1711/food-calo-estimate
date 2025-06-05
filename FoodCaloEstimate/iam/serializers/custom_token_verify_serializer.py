# Copyright (C)
# date: 05-06-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Custom Token Verify Serializer."""

from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class CustomTokenVerifySerializer(TokenVerifySerializer):
    """Custom Token Verify Serializer."""

    def validate(self, attrs: dict[str, None]) -> dict[Any, Any]:
        """Validate the token."""
        token = AccessToken(attrs["token"])
        try:
            user = User.objects.get(token.payload.get("user_id"))
        except:
            raise serializers.ValidationError("Token is invalid or expired.")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive.")
        return super().validate(attrs)
