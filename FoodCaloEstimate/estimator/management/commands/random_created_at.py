# Copyright (C)
# date: 24-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Random Created At Command."""

import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from FoodCaloEstimate.estimator.models.my_input_image import MyInputImage

DAYS_AGO = 7
BATCH_SIZE = 1000
update_fields = ["created_at", "updated_at", "deleted_at"]


def random_datetime_between(start, end):
    """
    Return a random datetime between start and end.
    """
    delta = end - start
    seconds = int(delta.total_seconds())
    return start + timedelta(seconds=random.randint(0, seconds))


def shuffle_timestamps():
    now = timezone.now()
    cutoff = now - timedelta(days=DAYS_AGO)

    qs = MyInputImage.objects.select_related("user").all()
    batch = []

    for img in qs.iterator(chunk_size=BATCH_SIZE):
        # calculate earliest_time not before user creation date and not more than DAYS_AGO before
        earliest = max(cutoff, img.user.date_joined)

        img.created_at = random_datetime_between(earliest, now)
        img.updated_at = random_datetime_between(img.created_at, now)
        img.deleted_at = (
            random_datetime_between(img.created_at, now) if img.is_deleted else None
        )

        batch.append(img)
        if len(batch) >= BATCH_SIZE:
            MyInputImage.objects.bulk_update(batch, update_fields)
            batch.clear()

    # bulk_update remaining items
    if batch:
        MyInputImage.objects.bulk_update(batch, update_fields)


class Command(BaseCommand):  # random_created_at
    """Command."""

    def handle(self, *args, **kwargs):
        """Handle."""
        shuffle_timestamps()
        self.stdout.write(self.style.SUCCESS("Successfully"))
