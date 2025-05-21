# Copyright (C)
# date: 21-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""User Profile Model."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from FoodCaloEstimate.iam.constants.user_constants import (
    DEFAULT_LENGTH_REFERENCE_POINT,
    DEFAULT_WIDTH_REFERENCE_POINT,
    MAX_LENGTH_REFERENCE_POINT,
    MAX_WIDTH_REFERENCE_POINT,
)
from FoodCaloEstimate.iam.models.base_model import AutoTimeStampedModel, UUIDModel

User = get_user_model()


class UserProfile(UUIDModel, AutoTimeStampedModel):
    """UserProfile model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    length_reference_point_custom = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        validators=[
            MinValueValidator(Decimal(0)),
            MaxValueValidator(Decimal(MAX_LENGTH_REFERENCE_POINT)),
        ],
    )
    width_reference_point_custom = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        validators=[
            MinValueValidator(Decimal(0)),
            MaxValueValidator(Decimal(MAX_WIDTH_REFERENCE_POINT)),
        ],
    )

    @property
    def length_reference_point(self) -> Decimal:
        """
        Trả về giá trị length: nếu user đã override, dùng custom,
        ngược lại lấy DEFAULT_LENGTH_REFERENCE_POINT.
        """
        if self.length_reference_point_custom is not None:
            return self.length_reference_point_custom
        # Chuyển DEFAULT sang Decimal nếu là float
        return Decimal(DEFAULT_LENGTH_REFERENCE_POINT)

    @property
    def width_reference_point(self) -> Decimal:
        """
        Trả về giá trị width: nếu user đã override, dùng custom,
        ngược lại lấy DEFAULT_WIDTH_REFERENCE_POINT.
        """
        if self.width_reference_point_custom is not None:
            return self.width_reference_point_custom
        return Decimal(DEFAULT_WIDTH_REFERENCE_POINT)

    @property
    def area_reference_point(self) -> Decimal:
        """
        Tính diện tích dựa trên length và width reference point (cm^2).
        """
        return self.length_reference_point * self.width_reference_point


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Tạo auto UserProfile khi User mới được tạo.
    """
    if created:
        UserProfile.objects.create(user=instance)
