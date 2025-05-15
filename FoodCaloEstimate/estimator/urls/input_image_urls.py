# Copyright (C)
# date: 12-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Input Image URLs."""

from rest_framework.routers import DefaultRouter

from FoodCaloEstimate.estimator.views.input_image_view_set import InputImageViewSet

router = DefaultRouter(trailing_slash=False)
router.register("", InputImageViewSet, basename="input_image")
urlpatterns = router.urls
