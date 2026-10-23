"""Sample delivery-network loading and route-planning helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

import streamlit as st

from algorithms.dijkstra import dijkstra

DistanceGraph: TypeAlias = dict[str, dict[str, float]]
Coordinates: TypeAlias = dict[str, dict[str, float]]
SAMPLE_NETWORK = Path(__file__).parent / "data" / "sample_network.json"


@dataclass(frozen=True)
class DeliveryRoute:
    """A route through one ordered set of required delivery stops."""

    locations: tuple[str, ...]
    distance_km: float
    start: str
    delivery_points: tuple[str, ...]
    destination: str


@st.cache_data
def load_sample_network() -> tuple[DistanceGraph, Coordinates]:
    """Load the illustrative road graph and map coordinates."""
    with SAMPLE_NETWORK.open(encoding="utf-8") as network_file:
        data = json.load(network_file)

    graph: DistanceGraph = {name: {} for name in data["locations"]}
    for road in data["roads"]:
        first = road["from"]
        second = road["to"]
        distance = float(road["distance"])
        graph[first][second] = distance
        graph[second][first] = distance

    coordinates: Coordinates = {
        name: {
            "latitude": float(point["latitude"]),
            "longitude": float(point["longitude"]),
        }
        for name, point in data["coordinates"].items()
    }
    if set(coordinates) != set(graph):
        raise ValueError("Every sample-network location must have map coordinates.")
    return graph, coordinates


def _route_distance(graph: DistanceGraph, locations: list[str]) -> float:
    return sum(
        graph[first][second]
        for first, second in zip(locations, locations[1:])
    )


def _combine_legs(legs: list[list[str]]) -> list[str]:
    route: list[str] = []
    for leg in legs:
        route.extend(leg if not route else leg[1:])
    return route


def _build_route(graph: DistanceGraph, checkpoints: list[str]) -> list[str]:
    legs: list[list[str]] = []
    for start, destination in zip(checkpoints, checkpoints[1:]):
        path, _ = dijkstra(graph, start, destination)
        if not path:
            raise ValueError(f"No road route exists from {start} to {destination}.")
        legs.append(path)
    return _combine_legs(legs)


def plan_route(
    graph: DistanceGraph,
    start: str,
    destination: str,
    delivery_points: list[str],
) -> DeliveryRoute:
    """Plan ordered delivery stops using the project's Dijkstra implementation."""
    if start not in graph or destination not in graph:
        raise ValueError("The start and destination must both exist in the network.")
    if any(point not in graph for point in delivery_points):
        raise ValueError("Every delivery point must exist in the network.")
    if len(set(delivery_points)) != len(delivery_points):
        raise ValueError("Delivery points cannot contain duplicates.")
    if start in delivery_points or destination in delivery_points:
        raise ValueError("The start and destination cannot also be delivery points.")

    locations = _build_route(graph, [start, *delivery_points, destination])
    return DeliveryRoute(
        locations=tuple(locations),
        distance_km=_route_distance(graph, locations),
        start=start,
        delivery_points=tuple(delivery_points),
        destination=destination,
    )


def route_directions(
    graph: DistanceGraph, route: tuple[str, ...]
) -> list[dict[str, str]]:
    """Convert a route into numbered, distance-labelled road instructions."""
    directions: list[dict[str, str]] = []
    for number, (first, second) in enumerate(zip(route, route[1:]), start=1):
        directions.append(
            {
                "step": str(number),
                "direction": f"Travel from {first} to {second}",
                "distance": f"{graph[first][second]:.1f} km",
            }
        )
    if len(route) == 1:
        directions.append(
            {
                "step": "1",
                "direction": f"You are already at {route[0]}",
                "distance": "0.0 km",
            }
        )
    return directions


def format_travel_time(distance_km: float, speed_kmh: float) -> str:
    """Format an average-speed estimate as hours and minutes."""
    total_minutes = round(distance_km / speed_kmh * 60)
    hours, minutes = divmod(total_minutes, 60)
    if hours and minutes:
        return f"{hours} hr {minutes} min"
    if hours:
        return f"{hours} hr"
    return f"{minutes} min"
