# Copyright (C)
# date: 09-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Init."""

# from django.urls import path, include
from FoodCaloEstimate.estimator.urls.input_image_urls import (
    urlpatterns as estimate_urls,
)

urlpatterns = [
    # custom prefix
    # path("", include(estimate_urls)),
] + estimate_urls
