# Copyright (C)
# date: 22-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Input Image Filter."""

from datetime import datetime, timedelta

import django_filters
from django.utils import timezone

from FoodCaloEstimate.estimator.models.my_input_image import MyInputImage
from FoodCaloEstimate.iam.constants.period_choices import MONTH_FORMAT, TimePeriod

MAX_WEEK = 9999


class InputImageFilter(django_filters.FilterSet):
    """Input Image Filter."""

    day = django_filters.DateFilter(field_name="created_at", lookup_expr="date")
    month = django_filters.CharFilter(method="filter_month")
    week = django_filters.NumberFilter(method="filter_week")

    class Meta:
        model = MyInputImage
        fields = [label for label in TimePeriod.labels]

    def filter_month(self, qs, name, value):
        try:
            d = datetime.strptime(value, MONTH_FORMAT)
        except:
            return qs.none()
        return qs.filter(created_at__year=d.year, created_at__month=d.month)

    def filter_week(self, queryset, name, idx):
        try:
            idx = int(idx)
        except:
            return queryset.none()
        if idx < 0 or idx >= MAX_WEEK:
            return queryset.none()

        today = timezone.now().date()
        start = today - timedelta(days=today.weekday()) - timedelta(weeks=idx)
        end = start + timedelta(days=TimePeriod.WEEK - 1)
        return queryset.filter(
            created_at__date__gte=start,
            created_at__date__lte=end,
        )

    def filter_queryset(self, queryset):
        """Filter queryset."""
        params = [self.data.get(param) for param in TimePeriod.labels]
        if sum(1 for p in params if p is not None) > 1:
            return queryset.none()
        return super().filter_queryset(queryset)
