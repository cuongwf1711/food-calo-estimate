# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Password Validator."""

from django.core.validators import RegexValidator


def password_validator(min_length=8, max_length=128):
    """Password validator."""
    return RegexValidator(
        regex=rf"^(?=.*[A-Za-z])(?=.*\d).{{{min_length},{max_length}}}$",
        message=f"This field must contain at least one letter, one digit, and be between {min_length} and {max_length} characters long.",
    )
