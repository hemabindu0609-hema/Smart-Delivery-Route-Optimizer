"""Stable, recursive Merge Sort implementation."""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def merge_sort(values: list[T]) -> list[T]:
    """Return a sorted copy of ``values`` without modifying the input."""
    if len(values) <= 1:
        return values.copy()
    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    merged: list[T] = []
    left_index = right_index = 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged
