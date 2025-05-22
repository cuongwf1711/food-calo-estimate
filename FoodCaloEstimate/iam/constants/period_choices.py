# Copyright (C)
# date: 22-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Period Choices Constants."""

from django.db import models


class TimePeriod(models.IntegerChoices):
    """Time Period Choices."""

    DAY = 1, "day"
    WEEK = 7, "week"
    MONTH = 30, "month"

    @classmethod
    def from_label(cls, label: str) -> int:
        for item in cls:
            if item.label == label:
                return item.value
        raise ValueError(f"Invalid period label: {label}")


PERIOD_CHOICES = tuple((item.label, item.label) for item in TimePeriod)


MAX_LENGTH_PERIOD = max(len(choice_value) for choice_value, _ in PERIOD_CHOICES)
