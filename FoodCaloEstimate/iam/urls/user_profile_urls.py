# Copyright (C)
# date: 22-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""User Profile URLs."""

from django.urls import path

from FoodCaloEstimate.iam.views.user_profile_view import UserProfileView

urlpatterns = [
    path("/user-profile", UserProfileView.as_view(), name="user-profile"),
]
