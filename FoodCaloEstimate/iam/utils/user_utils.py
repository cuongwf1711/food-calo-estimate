# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""User utils."""

from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError

from FoodCaloEstimate.messages.iam_messages import ACCOUNT_NOT_EXIST, INACTIVE_ACCOUNT

User = get_user_model()


def get_valid_user_or_raise_exeption(email):
    """Get valid user."""
    try:
        user = User.objects.get(username=email)
    except:
        raise ValidationError(ACCOUNT_NOT_EXIST)

    if not user.is_active:
        raise ValidationError(INACTIVE_ACCOUNT)

    return user
