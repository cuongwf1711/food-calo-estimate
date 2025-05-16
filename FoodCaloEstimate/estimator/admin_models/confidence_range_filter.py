# Copyright (C)
# date: 15-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Confidence Range Filter."""

from django.contrib.admin import SimpleListFilter

from FoodCaloEstimate.estimator.constants.admin_model_constants import TEMPLATE_DROPDOWN_FILTER


class ConfidenceRangeFilter(SimpleListFilter):
    """Filters by confidence percentage range."""

    title = "Confidence Range"
    parameter_name = "confidence"
    template = TEMPLATE_DROPDOWN_FILTER

    def lookups(self, request, model_admin):
        """Return the filter options."""
        return [
            ("lt25", "<25%"),
            ("25_50", "25-50%"),
            ("51_75", "51-75%"),
            ("gt75", ">75%"),
        ]

    def queryset(self, request, queryset):
        """Filter the queryset based on the selected range."""
        ranges = {
            "lt25": queryset.filter(confidence__lt=0.25),
            "25_50": queryset.filter(confidence__range=(0.25, 0.50)),
            "51_75": queryset.filter(confidence__range=(0.51, 0.75)),
            "gt75": queryset.filter(confidence__gt=0.75),
        }
        return ranges.get(self.value(), queryset)
