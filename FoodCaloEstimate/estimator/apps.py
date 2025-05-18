from django.apps import AppConfig

from FoodCaloEstimate.estimator.machine_learning_models.model_manager import (
    ModelManager,
)


class EstimatorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "FoodCaloEstimate.estimator"

    def ready(self):
        """Ready."""
        import atexit

        atexit.register(ModelManager.release_models)
