# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Messages module."""

from FoodCaloEstimate.iam.constants.auth_constants import OTP_EXPIRE

EXISTED_ACOUNT = "Account already exists. Please log in."
OTP_SENT = f"An OTP has already been sent. Please check your email or try again in {OTP_EXPIRE // 60} minutes."
OTP_EXPIRED = "OTP expired. Please request a new OTP."
OTP_INVALID = "Invalid OTP. Please check your email or request a new OTP."
EMAIL_SENT = "Email sent successfully. Please check your inbox."
ACCOUNT_SET_PASSWORD_SUCCESS = "Account set password successfully. Please sign in."
ACCOUNT_SIGN_UP_SUCCESS = (
    "Account sign up successfully. Please check your email to verify your account."
)
INACTIVE_ACCOUNT = "Your account is inactive."
ACCOUNT_NOT_EXIST = "Account does not exist."
CHANGE_PASSWORD_SUCCESS = "Password changed successfully."
INCORRECT_OLD_PASSWORD = "Old password is incorrect."
SAME_OLD_NEW_PASSWORD = "The new password and old password must not be the same."
RESET_PASSWORD_SUCCESS = "Password reset successfully. Please sign in."
