# Copyright (C)
# date: 09-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""User Model."""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Account model with custom fields."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        """Return username."""
        return self.username
