
"""Dijkstra's shortest-path algorithm using Python's heap-based priority queue."""

from __future__ import annotations

import heapq
from math import inf
from numbers import Real
from typing import Mapping

from algorithms._validation import validate_weighted_graph


def dijkstra(
    graph: Mapping[str, Mapping[str, Real]], start: str, destination: str
) -> tuple[list[str], float]:
    """Return the shortest path and distance; return ``([], inf)`` if unreachable.

    Edge weights must be finite and non-negative. Identical endpoints produce
    a zero-length route containing that location.
    """
    validate_weighted_graph(graph, allow_negative=False)
    if (
        not isinstance(start, str)
        or not isinstance(destination, str)
        or start not in graph
        or destination not in graph
    ):
        raise ValueError("Start and destination must both exist in the graph.")
    if start == destination:
        return [start], 0.0

    distances = {location: inf for location in graph}
    previous: dict[str, str | None] = {location: None for location in graph}
    distances[start] = 0.0
    priority_queue: list[tuple[float, str]] = [(0.0, start)]

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)
        if current_distance > distances[current]:
            continue
        if current == destination:
            break
        for neighbor, weight in graph[current].items():
            new_distance = current_distance + float(weight)
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
                heapq.heappush(priority_queue, (new_distance, neighbor))

    if distances[destination] == inf:
        return [], inf

    path: list[str] = []
    current: str | None = destination
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path, distances[destination]
