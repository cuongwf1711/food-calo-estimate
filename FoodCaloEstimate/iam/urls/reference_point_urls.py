# Copyright (C)
# date: 21-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Reference Point Urls."""

from django.urls import path

from FoodCaloEstimate.iam.views.reference_point_view import ReferencePointView

urlpatterns = [
    path("/reference-point", ReferencePointView.as_view(), name="get-reference-point"),
]
