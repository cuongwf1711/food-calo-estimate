# Copyright (C)
# date: 22-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""User Profile Serializer."""

from django.db.models import Sum
from django.utils import timezone
from rest_framework import serializers

from FoodCaloEstimate.estimator.models.my_input_image import MyInputImage
from FoodCaloEstimate.estimator.view_filters.input_image_filter import InputImageFilter
from FoodCaloEstimate.iam.constants.period_choices import (
    DAY_FORMAT,
    MONTH_FORMAT,
    TimePeriod,
)
from FoodCaloEstimate.iam.models.user_profile import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """User Profile Serializer."""

    auto_set_calorie_limit = serializers.BooleanField(write_only=True, required=False)
    total_calories = serializers.SerializerMethodField()

    def get_total_calories(self, obj):
        """Get total calories."""
        qs = MyInputImage.objects.filter(user=obj.user, is_deleted=False)
        now = timezone.now().date()
        period = obj.calorie_limit_period

        params = dict()
        if period in TimePeriod.DAY.label:
            params["day"] = now.strftime(DAY_FORMAT)
        elif period == TimePeriod.WEEK.label:
            params["week"] = 0
        elif period == TimePeriod.MONTH.label:
            params["month"] = now.strftime(MONTH_FORMAT)
        else:
            return 0.0

        filtered_qs = InputImageFilter(data=params, queryset=qs).qs
        return filtered_qs.aggregate(total=Sum("calo"))["total"] or 0.0

    class Meta:
        model = UserProfile
        fields = [
            "gender",
            "age",
            "height",
            "weight",
            "calorie_limit",
            "calorie_limit_period",
            "length_reference_point",
            "width_reference_point",
            "area_reference_point",
            "length_reference_point_custom",
            "width_reference_point_custom",
            "auto_set_calorie_limit",
            "total_calories",
        ]

        extra_kwargs = {
            "length_reference_point_custom": {"write_only": True},
            "width_reference_point_custom": {"write_only": True},
        }

    def update(self, instance, validated_data):
        if validated_data.pop("auto_set_calorie_limit", False):
            validated_data["calorie_limit"] = instance.calculate_auto_calorie_limit()

        return super().update(instance, validated_data)
