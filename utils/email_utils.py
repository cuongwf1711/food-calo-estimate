# Copyright (C)
# date: 09-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Email utility functions for sending emails."""

import logging
import os
from datetime import datetime
from email.mime.image import MIMEImage
from pathlib import Path

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from FoodCaloEstimate.iam.constants.general_constants import AUTHOR


class EmailService:
    """Utility for building and sending emails with attachments and inline images."""

    # Default images to include in all emails
    DEFAULT_IMAGES = [
        "logo_dut_50.jpg",
        "logo_dut.jpg",
        "logo_itf.jpg",
        "my_avatar.jpg",
    ]

    def __init__(
        self,
        subject: str,
        template: str,
        context: dict,
        to_addrs: list[str],
        images: list[str] | None = None,
        files: list[dict] | None = None,
        language: str = settings.LANGUAGE_CODE,
        use_queue: bool = True,
    ):
        self.subject = subject
        self.template = template
        self.context = context
        self.to_addrs = to_addrs or []

        # Combine custom images with default images, avoiding duplicates
        custom_images = images or []
        self.images = list(set(custom_images + self.DEFAULT_IMAGES))

        self.files = files or []
        self.language = language
        self.use_queue = use_queue

    def send(self):
        """Send."""
        # FIXME: Remove this print statement in production
        print(self.context)
        return
        self._build_context()
        html = render_to_string(self.template, self.context)
        text = strip_tags(html)

        email = EmailMultiAlternatives(
            self.subject,
            text,
            to=self.to_addrs,
        )

        # Attach files
        for f in self.files:
            with open(f["path"], "rb") as fp:
                email.attach(f["name"], fp.read(), f.get("content_type"))

            if os.path.exists(f.get("path")):
                os.remove(f.get("path"))

        # Attach HTML and images
        email.attach_alternative(html, "text/html")
        email.mixed_subtype = "related"

        img_dir = os.path.join(settings.BASE_DIR, "images")
        for index, img_name in enumerate(self.images):
            image_path = os.path.join(img_dir, img_name)
            try:
                with open(image_path, "rb") as fr:
                    img = MIMEImage(fr.read())
                    img.add_header("Content-ID", f"<{img_name}>")
                    img.add_header(
                        "Content-Disposition",
                        "inline",
                        filename=f"image{index}{Path(img_name).suffix}",
                    )
                    email.attach(img)
            except FileNotFoundError as err:
                logging.error(f"Image not found: {img}. Error: {err}")

        email.send()

    def _build_context(self):
        self.context["current_year"] = datetime.now().year
        self.context["email"] = settings.CONTACT_EMAIL
        self.context["author"] = AUTHOR
