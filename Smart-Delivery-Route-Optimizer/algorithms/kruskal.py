"""Kruskal's minimum spanning forest algorithm with a disjoint-set structure."""

from __future__ import annotations

from numbers import Real
from typing import Mapping

from algorithms._validation import validate_weighted_graph
from algorithms.prim import MSTResult


def kruskal_mst(graph: Mapping[str, Mapping[str, Real]]) -> MSTResult:
    """Return forest edges, total weight, and whether the graph is connected."""
    validate_weighted_graph(graph, allow_negative=True, require_undirected=True)
    parent = {location: location for location in graph}
    rank = {location: 0 for location in graph}

    def find(location: str) -> str:
        while parent[location] != location:
            parent[location] = parent[parent[location]]
            location = parent[location]
        return location

    def union(first: str, second: str) -> bool:
        first_root, second_root = find(first), find(second)
        if first_root == second_root:
            return False
        if rank[first_root] < rank[second_root]:
            first_root, second_root = second_root, first_root
        parent[second_root] = first_root
        if rank[first_root] == rank[second_root]:
            rank[first_root] += 1
        return True

    edges = sorted(
        (float(weight), first, second)
        for first, neighbors in graph.items()
        for second, weight in neighbors.items()
        if first < second
    )
    selected: list[tuple[str, str, float]] = []
    total_weight = 0.0
    for weight, first, second in edges:
        if union(first, second):
            selected.append((first, second, weight))
            total_weight += weight

    connected = len(graph) <= 1 or len(selected) == len(graph) - 1
    return selected, total_weight, connected
