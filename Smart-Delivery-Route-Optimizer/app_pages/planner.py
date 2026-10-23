"""Delivery route selection page."""

import streamlit as st

from delivery_routes import load_sample_network

graph, _ = load_sample_network()
locations = list(graph)
request = st.session_state.route_request

st.title("Route planner")
st.write(
    "Choose a starting point, destination, and any delivery locations to visit. "
    "Selected delivery locations are visited in the order shown."
)

with st.form("delivery_route_form"):
    start_col, destination_col = st.columns(2)
    start = start_col.selectbox(
        "Starting point",
        locations,
        index=locations.index(request["start"]),
    )
    destination = destination_col.selectbox(
        "Destination",
        locations,
        index=locations.index(request["destination"]),
    )
    available_points = [
        name for name in locations if name not in {start, destination}
    ]
    default_points = [
        point for point in request["delivery_points"] if point in available_points
    ]
    delivery_points = st.multiselect(
        "Delivery locations",
        available_points,
        default=default_points,
        help="These stops will be visited in the order selected.",
    )
    submitted = st.form_submit_button(
        "Save delivery plan",
        type="primary",
        icon=":material/save:",
        width="stretch",
    )

if submitted:
    st.session_state.route_request = {
        "start": start,
        "destination": destination,
        "delivery_points": delivery_points,
    }
    st.session_state.optimized_route = None
    st.success("Delivery plan saved. Run route optimization to calculate the shortest path.")

st.subheader("Selected delivery plan")
current_request = st.session_state.route_request
summary = [
    current_request["start"],
    *current_request["delivery_points"],
    current_request["destination"],
]
st.markdown("  →  ".join(summary))
st.page_link(
    "app_pages/optimization.py",
    label="Continue to route optimization",
    icon=":material/arrow_forward:",
)
