# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

import hashlib
import hmac
import time
import uuid

from django.conf import settings
from rest_framework.serializers import ValidationError

from FoodCaloEstimate.iam.constants.auth_constants import (
    OTP_DB_REDIS,
    OTP_EXPIRE,
    OTP_LENGTH,
)
from FoodCaloEstimate.iam.services.redis_services import RedisService
from FoodCaloEstimate.messages.iam_messages import OTP_EXPIRED, OTP_INVALID, OTP_SENT


def generate_otp(email: str, length: int = OTP_LENGTH) -> str:
    """Generate OTP."""
    timestamp = int(time.time() * 1000)
    salt = f"{email}|{timestamp}|{uuid.uuid4()}"

    key = settings.SECRET_KEY.encode()
    digest_bytes = hmac.new(key, salt.encode(), hashlib.sha256).digest()

    otp_int = int.from_bytes(digest_bytes, "big")
    otp_str = str(otp_int).zfill(length)
    return otp_str[-length:]


def set_otp_to_redis_or_raise_exception(email):
    """Set OTP to Redis or raise exception."""
    otp = generate_otp(email)
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
