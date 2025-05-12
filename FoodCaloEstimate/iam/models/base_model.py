# Copyright (C)
# date: 12-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Base Model."""

import uuid

from django.db import models


class UUIDModel(models.Model):
    """UUID model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """Meta class."""

        abstract = True


class SoftDeleteModel(models.Model):
    """Soft delete model."""

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Abstract model."""

        abstract = True


class AutoTimeStampedModel(models.Model):
    """Auto set created_at and updated_at fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Abstract model."""

        abstract = True
