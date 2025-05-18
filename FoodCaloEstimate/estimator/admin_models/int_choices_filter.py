# Copyright (C)
# date: 15-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Int Choices Filter."""


from django.contrib.admin import SimpleListFilter

from FoodCaloEstimate.estimator.constants.admin_model_constants import (
    TEMPLATE_DROPDOWN_FILTER,
)
from FoodCaloEstimate.estimator.services.food_dictionany_service import FoodDictionary


def make_int_choice_filter(field_name, title_text):
    """Make Int Choice Filter."""

    class IntChoiceFilter(SimpleListFilter):
        """Int Choice Filter."""

        title = title_text
        parameter_name = field_name
        template = TEMPLATE_DROPDOWN_FILTER

        def lookups(self, request, model_admin):
            """Lookups for the filter."""
            present = set(
                model_admin.get_queryset(request).values_list(field_name, flat=True)
            )

            return [
                (str(food_id), FoodDictionary.get_name(food_id)) for food_id in present
            ]

        def queryset(self, request, queryset):
            """Filter the queryset based on the selected value."""
            value = self.value()
            if not value:
                return queryset
            return queryset.filter(**{field_name: int(value)})

    return IntChoiceFilter
