# Copyright (C)
# date: 09-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""User Model."""


from django.contrib.auth.models import AbstractUser

from FoodCaloEstimate.iam.models.base_model import UUIDModel


class User(AbstractUser, UUIDModel):
    """Account model with custom fields."""

    def __str__(self):
        """Return username."""
        return self.username
