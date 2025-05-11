# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Redis services."""

import redis
from django.conf import settings


class RedisService:
    """Redis service."""

    def __init__(self, db):
        """Initialize Redis service."""
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=db,
            decode_responses=True,
            protocol=3,
        )

    def set(self, data_dict, overwrite=False, expire=None):
        """Set value in Redis."""
        keys = list(data_dict.keys())
        if not overwrite and self.redis_client.exists(*keys):
            return False
        with self.redis_client.pipeline() as pipe:
            for key, value in data_dict.items():
                pipe.set(key, value, ex=expire, nx=not overwrite)
            pipe.execute()
        return True

    def get(self, name):
        """Get value from Redis."""
        return self.redis_client.get(name)

    def delete(self, *args):
        """Delete value from Redis."""
        self.redis_client.delete(*args)
