"""Iterative binary search over an already sorted sequence."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def binary_search(sorted_values: Sequence[T], target: T) -> int:
    """Return an index containing ``target``, or -1 if it is absent.

    The sequence must already be sorted in ascending order.
    """
    low, high = 0, len(sorted_values) - 1
    while low <= high:
        middle = (low + high) // 2
        value = sorted_values[middle]
        if value == target:
            return middle
        if value < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1
