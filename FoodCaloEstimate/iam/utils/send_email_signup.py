# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Send Email Sign Up."""

from FoodCaloEstimate.iam.constants.auth_constants import OTP_EXPIRE
from FoodCaloEstimate.queue_tasks import run_task_in_queue
from utils.email_utils import EmailService


def send_email_signup(email, otp):
    """Send email sign up."""
    run_task_in_queue(
        EmailService(
            subject="Welcome",
            template="emails/main_email.html",
            context={
                "data": {
                    "Your OTP": otp,
                    f"Please use this code to activate your account. \
                        The code is valid for {OTP_EXPIRE // 60} minute. \
                        Do not share this code with anyone. \
                        If you did not request this, please ignore this email.": "",
                }
            },
            to_addrs=[email],
        ).send
    )
