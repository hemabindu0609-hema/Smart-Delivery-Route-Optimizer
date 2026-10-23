"""Shared validation for weighted adjacency-dictionary graphs."""

from __future__ import annotations

import math
from numbers import Real
from typing import Mapping


def validate_weighted_graph(
    graph: Mapping[str, Mapping[str, Real]],
    *,
    allow_negative: bool,
    require_undirected: bool = False,
) -> None:
    """Check graph shape, finite numeric weights, and optionally symmetry."""
    if not isinstance(graph, Mapping):
        raise ValueError("Graph must be a mapping of locations to neighbors.")
    for location, neighbors in graph.items():
        if not isinstance(location, str) or not location:
            raise ValueError("Location names must be non-empty strings.")
        if not isinstance(neighbors, Mapping):
            raise ValueError(f"Neighbors for {location!r} must be a mapping.")
        for neighbor, weight in neighbors.items():
            if neighbor not in graph:
                raise ValueError(f"Neighbor {neighbor!r} is not a graph location.")
            if isinstance(weight, bool) or not isinstance(weight, Real):
                raise ValueError("Edge weights must be real numbers.")
            if not math.isfinite(float(weight)):
                raise ValueError("Edge weights must be finite.")
            if not allow_negative and weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights.")
            if require_undirected and graph[neighbor].get(location) != weight:
                raise ValueError("Minimum spanning tree algorithms require symmetric undirected edges.")
