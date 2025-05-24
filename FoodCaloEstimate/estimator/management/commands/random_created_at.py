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


def random_datetime_between(start, end):
    """
    Return a random datetime between start and end.
    """
    delta = end - start
    seconds = int(delta.total_seconds())
    return start + timedelta(seconds=random.randint(0, seconds))


def shuffle_timestamps():
    """Shuffle timestamps."""
    now = timezone.now()
    month_ago = now - timedelta(days=DAYS_AGO)

    for img in MyInputImage.objects.all():
        # pick new created_at
        new_created = random_datetime_between(month_ago, now)

        # pick new updated_at (>= created_at, <= now)
        new_updated = random_datetime_between(new_created, now)

        # determine deleted_at
        if img.is_deleted:
            # deleted_at between created_at and now
            new_deleted = random_datetime_between(new_created, now)
        else:
            new_deleted = None

        # apply via QuerySet.update to bypass auto_now / auto_now_add
        MyInputImage.objects.filter(pk=img.pk).update(
            created_at=new_created, updated_at=new_updated, deleted_at=new_deleted
        )


class Command(BaseCommand):  # random_created_at
    """Command."""

    def handle(self, *args, **kwargs):
        """Handle."""
        shuffle_timestamps()
        self.stdout.write(self.style.SUCCESS("Successfully"))
