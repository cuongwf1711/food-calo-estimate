# Copyright (C)
# date: 09-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Auth Urls."""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from FoodCaloEstimate.iam.views.change_password_view import ChangePasswordView
from FoodCaloEstimate.iam.views.forgot_password_view import ForgotPasswordView
from FoodCaloEstimate.iam.views.resend_email_view import ResendEmailView
from FoodCaloEstimate.iam.views.set_password_view import SetPasswordView
from FoodCaloEstimate.iam.views.sign_up_email_view import SiginUpEmailView

urlpatterns = [
    path("", TokenObtainPairView.as_view(), name="sigin"),
    path("/refresh-token", TokenRefreshView.as_view(), name="refresh-token"),
    path("/verify-token", TokenVerifyView.as_view(), name="token_verify"),
    path("/signup", SiginUpEmailView.as_view(), name="signup"),
    path("/set-password", SetPasswordView.as_view(), name="set-password"),
    path("/resend-email", ResendEmailView.as_view(), name="resend-email"),
    path("/change-password", ChangePasswordView.as_view(), name="change-password"),
    path("/forgot-password", ForgotPasswordView.as_view(), name="forgot-password"),
]
