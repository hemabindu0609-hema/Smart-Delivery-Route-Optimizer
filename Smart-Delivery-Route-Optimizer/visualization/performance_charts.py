"""Matplotlib charts for measured algorithm benchmark results."""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib.pyplot as plt
import streamlit as st


def draw_benchmark_chart(results: Sequence[dict[str, float]]) -> None:
    """Display measured execution time against graph size."""
    if not results:
        return
    figure, axis = plt.subplots(figsize=(9, 4.6), dpi=120)
    figure.patch.set_facecolor("#f7f9fc")
    axis.set_facecolor("#ffffff")
    sizes = [row["Locations"] for row in results]
    axis.plot(sizes, [row["Dijkstra (ms)"] for row in results],
              marker="o", linewidth=2.5, color="#2f6fed", label="Dijkstra")
    axis.plot(sizes, [row["Bellman-Ford (ms)"] for row in results],
              marker="s", linewidth=2.5, color="#ef8a48", label="Bellman–Ford")
    axis.set_title("Empirical shortest-path execution time", loc="left",
                   color="#12233f", fontweight="bold", pad=14)
    axis.set_xlabel("Graph size (locations)")
    axis.set_ylabel("Median execution time (ms)")
    axis.grid(axis="y", color="#e7edf5", linewidth=0.8)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(frameon=False)
    figure.tight_layout()
    st.pyplot(figure, width="stretch")
    plt.close(figure)
