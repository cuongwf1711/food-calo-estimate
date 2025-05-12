# Copyright (C)
# date: 09-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Command to create default user."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):  # create_default_user
    """Create default user."""

    def create_or_update_user(
        self, username, password, is_superuser=False, is_staff=False
    ):
        """Create or update user."""
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"is_superuser": is_superuser, "is_staff": is_staff},
        )
        if not created:
            user.set_password(password)
            user.is_superuser = is_superuser
            user.is_staff = is_staff
        else:
            user.set_password(password)
        user.save()

    def handle(self, *args, **kwargs):
        """Create default user."""
        self.create_or_update_user(
            username=settings.DUMMY_USERNAME,
            password=settings.DUMMY_PASSWORD,
        )

        self.create_or_update_user(
            username=settings.ADMIN_USERNAME,
            password=settings.ADMIN_PASSWORD,
            is_superuser=True,
            is_staff=True,
        )

        self.stdout.write(self.style.SUCCESS("Create Default User Successfully."))
