# Copyright (C)
# date: 19-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Run try loop functions."""

from typing import Any, Callable, List


class AggregateException(Exception):
    """
    Exception to aggregate multiple exceptions.
    """

    def __init__(self, exceptions: List[Exception]):
        self.exceptions = exceptions
        msgs = "\n".join(
            f"{i+1}. {type(e).__name__}: {e}" for i, e in enumerate(exceptions)
        )
        super().__init__(f"Multiple exceptions occurred:\n{msgs}")


def run_try_loop_funcs(
    funcs: List[Callable[..., Any]], *args: Any, **kwargs: Any
) -> Any:
    """Run try loop functions."""
    errors: List[Exception] = []
    for func in funcs:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            errors.append(e)
    raise AggregateException(errors if errors else [Exception("No functions provided")])
