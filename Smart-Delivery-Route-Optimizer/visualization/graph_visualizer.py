"""Matplotlib drawing helper for the delivery graph."""

from __future__ import annotations

from collections.abc import Mapping

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st
from matplotlib.lines import Line2D


def draw_network(
    adjacency: Mapping[str, Mapping[str, float]],
    route: list[str] | None = None,
    start: str | None = None,
    destination: str | None = None,
) -> None:
    """Render an undirected, distance-labelled graph and optional route highlight."""
    graph = nx.Graph()
    graph.add_nodes_from(adjacency)
    for location, neighbors in adjacency.items():
        for neighbor, distance in neighbors.items():
            if location < neighbor:
                graph.add_edge(location, neighbor, weight=distance)

    if graph.number_of_nodes() == 0:
        st.info("The network is empty. Add locations in Route Planner to get started.")
        return

    positions = nx.spring_layout(graph, seed=17, k=1.1)
    figure, axis = plt.subplots(figsize=(12, 6.5), dpi=120)
    figure.patch.set_facecolor("#f7f9fc")
    axis.set_facecolor("#f7f9fc")

    route_edges = {
        frozenset((first, second))
        for first, second in zip(route or [], (route or [])[1:])
    }
    normal_edges = [
        edge for edge in graph.edges
        if frozenset(edge) not in route_edges
    ]
    highlighted_edges = [
        edge for edge in graph.edges
        if frozenset(edge) in route_edges
    ]

    nx.draw_networkx_edges(
        graph, positions, edgelist=normal_edges, width=1.7,
        edge_color="#a8b7cb", alpha=0.9, ax=axis,
    )
    nx.draw_networkx_edges(
        graph, positions, edgelist=highlighted_edges, width=4,
        edge_color="#2f6fed", ax=axis,
    )
    node_colors = [
        "#21a179" if node == start else "#ef6b5b" if node == destination else "#dce9ff"
        for node in graph.nodes
    ]
    nx.draw_networkx_nodes(
        graph, positions, node_color=node_colors, node_size=1250,
        edgecolors="#ffffff", linewidths=2.2, ax=axis,
    )
    nx.draw_networkx_labels(
        graph, positions, font_size=8.5, font_weight="bold",
        font_color="#12233f", ax=axis,
    )
    nx.draw_networkx_edge_labels(
        graph, positions,
        edge_labels={edge: f"{data['weight']:g} km" for edge, data in graph.edges.items()},
        font_size=8, font_color="#344a68", rotate=False,
        bbox={"alpha": 0.82, "color": "#f7f9fc", "pad": 1},
        ax=axis,
    )
    legend = [
        Line2D([0], [0], marker="o", color="w", label="Location",
               markerfacecolor="#dce9ff", markeredgecolor="#9dbbe8", markersize=11),
        Line2D([0], [0], color="#a8b7cb", linewidth=2, label="Road"),
        Line2D([0], [0], color="#2f6fed", linewidth=4, label="Selected shortest route"),
    ]
    if start:
        legend.append(Line2D([0], [0], marker="o", color="w", label="Start",
                             markerfacecolor="#21a179", markersize=10))
    if destination:
        legend.append(Line2D([0], [0], marker="o", color="w", label="Destination",
                             markerfacecolor="#ef6b5b", markersize=10))
    axis.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, -0.03),
                ncol=min(len(legend), 5), frameon=False, fontsize=8)
    axis.margins(0.18)
    axis.axis("off")
    figure.tight_layout()
    st.pyplot(figure, width="stretch")
    plt.close(figure)
