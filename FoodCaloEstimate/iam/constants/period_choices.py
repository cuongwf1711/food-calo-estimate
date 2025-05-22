# Copyright (C)
# date: 22-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Period Choices Constants."""


PERIOD_DAY = "day"
PERIOD_WEEK = "week"
PERIOD_MONTH = "month"

PERIOD_CHOICES = (
    (PERIOD_DAY, "day"),
    (PERIOD_WEEK, "week"),
    (PERIOD_MONTH, "month"),
)

MAX_LENGTH_PERIOD = max(len(choice_value) for choice_value, _ in PERIOD_CHOICES)
