# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

import secrets

from rest_framework.serializers import ValidationError

from FoodCaloEstimate.iam.constants.auth_constants import (
    OTP_DB_REDIS,
    OTP_EXPIRE,
    OTP_LENGTH,
)
from FoodCaloEstimate.iam.services.redis_services import RedisService
from FoodCaloEstimate.messages.iam_messages import OTP_EXPIRED, OTP_INVALID, OTP_SENT


def generate_otp(length=OTP_LENGTH):
    """Generate OTP."""
    return "".join(secrets.choice("0123456789") for _ in range(length))


def set_otp_to_redis_or_raise_exception(email):
    """Set OTP to Redis or raise exception."""
    otp = generate_otp()
    if not RedisService(OTP_DB_REDIS).set(
        {
            email: otp,
        },
        expire=OTP_EXPIRE,
    ):
        raise ValidationError(OTP_SENT)
    return otp


def check_valid_client_otp_or_raise_exception(email, otp):
    """Check valid client OTP or raise exception."""
    server_otp = RedisService(OTP_DB_REDIS).get(email)
    if not server_otp:
        raise ValidationError(OTP_EXPIRED)
    if server_otp != otp:
        raise ValidationError(OTP_INVALID)
