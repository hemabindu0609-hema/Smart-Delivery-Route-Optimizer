"""Interactive map of the optimized delivery route."""

import streamlit as st

from delivery_routes import load_sample_network
from visualization.delivery_map import show_delivery_map

_, coordinates = load_sample_network()
route = st.session_state.optimized_route

st.title("Route map")
st.write("Explore the delivery locations and the calculated shortest route.")

if route is None:
    st.info("Save a delivery plan and calculate its shortest route to display the map.")
    st.page_link(
        "app_pages/optimization.py",
        label="Go to route optimization",
        icon=":material/route:",
    )
else:
    with st.container(border=True):
        show_delivery_map(
            coordinates,
            route,
            start=route.start,
            destination=route.destination,
            delivery_points=route.delivery_points,
            key="optimized_route_map",
        )
    st.caption(
        "Sample locations and coordinates are illustrative. The highlighted route "
        "uses the project's road-distance data."
    )
