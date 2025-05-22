# Copyright (C)
# date: 12-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Abstract Input Image."""

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from FoodCaloEstimate.estimator.constants.image_constants import UNKNOWN_INDEX
from FoodCaloEstimate.iam.constants.django_model_constant import MAX_LENGTH_CHAR_FIELD
from FoodCaloEstimate.iam.models.base_model import (
    AutoTimeStampedModel,
    SoftDeleteModel,
    UUIDModel,
)

User = get_user_model()


class AbstractInputImage(AutoTimeStampedModel, UUIDModel, SoftDeleteModel):
    """Abstract Input Image."""

    url = models.JSONField()
    label = models.IntegerField(default=UNKNOWN_INDEX)
    predict = models.IntegerField(default=UNKNOWN_INDEX)
    confidence = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="uploaded_images"
    )
    staff = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="labeled_images", null=True
    )
    comment = models.CharField(max_length=MAX_LENGTH_CHAR_FIELD, blank=True)

    def __str__(self):
        """String representation of the model."""
        return str(self.id)

    @property
    def confidence_percentage(self):
        """Return confidence as a formatted percentage."""
        return f"{self.confidence * 100:.2f}%"

    class Meta:
        """Meta class for AbstractInputImage."""

        abstract = True
        ordering = ["-created_at"]
