# Copyright (C)
# date: 09-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Init."""

from django.urls import path, include

from FoodCaloEstimate.iam.urls import auth_urls


urlpatterns = [
    path("/auth", include(auth_urls), name="auth"),
]
