# Copyright (C)
# date: 12-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""My Input Image."""

from django.db import models

from FoodCaloEstimate.estimator.models import AbstractInputImage


class MyInputImage(AbstractInputImage):
    """My Input Image."""

    calo = models.FloatField()
