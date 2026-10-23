"""Bellman–Ford shortest-path algorithm with reachable negative-cycle detection."""

from __future__ import annotations

from math import inf
from numbers import Real
from typing import Mapping

from algorithms._validation import validate_weighted_graph


def bellman_ford(
    graph: Mapping[str, Mapping[str, Real]], start: str, destination: str
) -> tuple[list[str], float]:
    """Return shortest path and distance, supporting negative edge weights.

    Returns ``([], inf)`` if the destination is unreachable. Raises ValueError
    if a negative-weight cycle reachable from ``start`` makes paths undefined.
    """
    validate_weighted_graph(graph, allow_negative=True)
    if (
        not isinstance(start, str)
        or not isinstance(destination, str)
        or start not in graph
        or destination not in graph
    ):
        raise ValueError("Start and destination must both exist in the graph.")

    distances = {location: inf for location in graph}
    previous: dict[str, str | None] = {location: None for location in graph}
    distances[start] = 0.0
    for _ in range(max(0, len(graph) - 1)):
        changed = False
        for source, neighbors in graph.items():
            if distances[source] == inf:
                continue
            for target, weight in neighbors.items():
                candidate = distances[source] + float(weight)
                if candidate < distances[target]:
                    distances[target] = candidate
                    previous[target] = source
                    changed = True
        if not changed:
            break

    for source, neighbors in graph.items():
        if distances[source] == inf:
            continue
        for target, weight in neighbors.items():
            if distances[source] + float(weight) < distances[target]:
                raise ValueError("A reachable negative-weight cycle exists.")

    if distances[destination] == inf:
        return [], inf
    path: list[str] = []
    current: str | None = destination
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path, distances[destination]
