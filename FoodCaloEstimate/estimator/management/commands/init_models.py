# Copyright (C)
# date: 14-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Init Models."""

from django.core.management.base import BaseCommand

from FoodCaloEstimate.estimator.machine_learning_models.model_manager import (
    ModelManager,
)


class Command(BaseCommand):  # init_models
    """Command."""

    def handle(self, *args, **kwargs):
        """Handle."""
        ModelManager.initialize_models()
        self.stdout.write(self.style.SUCCESS("Init Models Successfully"))
