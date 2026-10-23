"""Prim's minimum spanning forest algorithm for undirected weighted graphs."""

from __future__ import annotations

import heapq
from numbers import Real
from typing import Mapping

from algorithms._validation import validate_weighted_graph

MSTResult = tuple[list[tuple[str, str, float]], float, bool]


def prim_mst(graph: Mapping[str, Mapping[str, Real]]) -> MSTResult:
    """Return forest edges, total weight, and whether the graph is connected.

    Disconnected input returns a minimum spanning forest. Empty and single-node
    graphs are considered connected and need no selected edges.
    """
    validate_weighted_graph(graph, allow_negative=True, require_undirected=True)
    visited: set[str] = set()
    selected: list[tuple[str, str, float]] = []
    total_weight = 0.0

    for root in sorted(graph):
        if root in visited:
            continue
        visited.add(root)
        candidates: list[tuple[float, str, str]] = [
            (float(weight), root, neighbor)
            for neighbor, weight in graph[root].items()
            if neighbor not in visited
        ]
        heapq.heapify(candidates)
        while candidates:
            weight, parent, node = heapq.heappop(candidates)
            if node in visited:
                continue
            visited.add(node)
            selected.append((parent, node, weight))
            total_weight += weight
            for neighbor, next_weight in graph[node].items():
                if neighbor not in visited:
                    heapq.heappush(candidates, (float(next_weight), node, neighbor))

    connected = len(graph) <= 1 or len(selected) == len(graph) - 1
    return selected, total_weight, connected
