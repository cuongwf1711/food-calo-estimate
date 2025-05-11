# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Split a string into a number and a string."""

from typing import Tuple


def split_num_str(s: str) -> Tuple[str, str]:
    """Split a string into a number and a string."""
    for i, char in enumerate(s):
        if not char.isdigit():
            return s[:i], s[i:]
    return s, ""
