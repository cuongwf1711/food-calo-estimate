# Copyright (C)
# date: 24-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Random Created At Command."""

import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from FoodCaloEstimate.estimator.models.my_input_image import MyInputImage

User = get_user_model()

DAYS_AGO = 7
BATCH_SIZE = 1000
IMG_UPDATE_FIELDS = ["created_at", "updated_at", "deleted_at"]
USER_UPDATE_FIELDS = ["date_joined", "last_login"]


def random_datetime_between(start, end):
    """
    Return a random datetime between start and end.
    """
    delta = end - start
    seconds = int(delta.total_seconds())
    return start + timedelta(seconds=random.randint(0, seconds))


def shuffle_timestamps(randomize_users=False):
    now = timezone.now()
    cutoff = now - timedelta(days=DAYS_AGO)

    user_count = 0
    img_count = 0

    # Optionally shuffle user timestamps first
    if randomize_users:
        users = User.objects.all()
        user_batch = []
        for user in users.iterator(chunk_size=BATCH_SIZE):
            # new_join = random_datetime_between(cutoff, now)
            # new_join = cutoff
            new_login = random_datetime_between(new_join, now)
            user.date_joined = new_join
            user.last_login = new_login
            user_batch.append(user)
            user_count += 1
            if len(user_batch) >= BATCH_SIZE:
                User.objects.bulk_update(user_batch, USER_UPDATE_FIELDS)
                user_batch.clear()
        if user_batch:
            User.objects.bulk_update(user_batch, USER_UPDATE_FIELDS)
            user_batch.clear()

    # Shuffle image timestamps
    qs = MyInputImage.objects.select_related("user").all()
    img_batch = []

    for img in qs.iterator(chunk_size=BATCH_SIZE):
        earliest = max(cutoff, img.user.date_joined)
        img.created_at = random_datetime_between(earliest, now)
        img.updated_at = random_datetime_between(img.created_at, now)
        img.deleted_at = (
            random_datetime_between(img.created_at, now) if img.is_deleted else None
        )
        img_batch.append(img)
        img_count += 1
        if len(img_batch) >= BATCH_SIZE:
            MyInputImage.objects.bulk_update(img_batch, IMG_UPDATE_FIELDS)
            img_batch.clear()
    if img_batch:
        MyInputImage.objects.bulk_update(img_batch, IMG_UPDATE_FIELDS)
        img_batch.clear()

    return img_count, user_count


class Command(BaseCommand):  # random_created_at
    """Command."""

    def handle(self, *args, **kwargs):
        """Handle."""
        randomize_users = True
        img_count, user_count = shuffle_timestamps(randomize_users=randomize_users)
        msg = f"Shuffled {img_count} image records."
        if randomize_users:
            msg += f" Shuffled {user_count} user records."
        self.stdout.write(self.style.SUCCESS(msg))
