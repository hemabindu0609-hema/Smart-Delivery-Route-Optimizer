"""Optimized route details and step-by-step directions."""

import streamlit as st

from delivery_routes import (
    format_travel_time,
    load_sample_network,
    route_directions,
)

graph, _ = load_sample_network()
route = st.session_state.optimized_route
speed = st.session_state.average_speed

st.title("Route results")

if route is None:
    st.info("Calculate a route before viewing its results.")
    st.page_link(
        "app_pages/optimization.py",
        label="Go to route optimization",
        icon=":material/route:",
    )
else:
    st.write(
        f"Optimized journey from **{route.start}** to **{route.destination}**, "
        "including all selected delivery locations."
    )

    with st.container(horizontal=True):
        st.metric("Total distance", f"{route.distance_km:.1f} km", border=True)
        st.metric(
            "Estimated travel time",
            format_travel_time(route.distance_km, speed),
            border=True,
        )
        st.metric("Road segments", max(len(route.locations) - 1, 0), border=True)

    st.subheader("Final route")
    st.markdown("  →  ".join(route.locations))

    st.subheader("Step-by-step route details")
    for instruction in route_directions(graph, route.locations):
        with st.container(border=True):
            step_col, direction_col, distance_col = st.columns([0.6, 3, 1])
            step_col.markdown(f"**{instruction['step']}**")
            direction_col.write(instruction["direction"])
            distance_col.write(instruction["distance"])

    st.caption(
        f"Travel time is estimated at {speed} km/h. Stops, traffic, and road conditions are not included."
    )
