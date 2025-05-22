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

from FoodCaloEstimate.iam.constants.period_choices import (
    MAX_LENGTH_PERIOD,
    PERIOD_CHOICES,
    TimePeriod,
)
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
    gender = models.BooleanField(null=True)
    age = models.PositiveSmallIntegerField(null=True)
    height = models.PositiveSmallIntegerField(null=True)
    weight = models.PositiveSmallIntegerField(null=True)
    calorie_limit = models.FloatField(null=True)
    calorie_limit_period = models.CharField(
        max_length=MAX_LENGTH_PERIOD,
        choices=PERIOD_CHOICES,
        default=TimePeriod.DAY.label,
    )

    @property
    def length_reference_point(self) -> Decimal:
        """Length reference point."""
        if self.length_reference_point_custom is not None:
            return self.length_reference_point_custom
        return Decimal(DEFAULT_LENGTH_REFERENCE_POINT)

    @property
    def width_reference_point(self) -> Decimal:
        """Width reference point."""
        if self.width_reference_point_custom is not None:
            return self.width_reference_point_custom
        return Decimal(DEFAULT_WIDTH_REFERENCE_POINT)

    @property
    def area_reference_point(self) -> Decimal:
        """Area reference point."""
        return self.length_reference_point * self.width_reference_point

    def calculate_auto_calorie_limit(self):
        """Calculate calorie limit based on user profile."""
        if (
            self.gender is None
            or self.age is None
            or self.height is None
            or self.weight is None
        ):
            return self.calorie_limit

        # Calculate the base BMR using weight, height, and age
        # This part is common for both genders
        base_bmr_calculation = 10 * self.weight + 6.25 * self.height - 5 * self.age

        # Determine the gender-specific adjustment value
        # Add 5 for males, subtract 161 for females
        gender_specific_adjustment = 5 if self.gender else -161

        # Add the gender adjustment to the base BMR
        total_calculated_bmr_per_day = base_bmr_calculation + gender_specific_adjustment

        total_calculated_bmr = total_calculated_bmr_per_day * TimePeriod.from_label(
            self.calorie_limit_period
        )

        # Round the final BMR to two decimal places for accuracy
        final_bmr_value = round(total_calculated_bmr, 2)

        return final_bmr_value


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile when user is created."""
    if created:
        UserProfile.objects.create(user=instance)
