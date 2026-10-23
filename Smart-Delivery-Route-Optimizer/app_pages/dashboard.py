"""Delivery route dashboard."""

import streamlit as st

from delivery_routes import format_travel_time, load_sample_network

graph, _ = load_sample_network()
route = st.session_state.optimized_route
speed = st.session_state.average_speed

st.title("Delivery dashboard")
st.write("A clear view of your current delivery plan and optimized journey.")

with st.container(horizontal=True):
    st.metric("Delivery locations", len(graph), border=True)
    st.metric(
        "Optimized distance",
        f"{route.distance_km:.1f} km" if route else "Not optimized",
        border=True,
    )
    st.metric(
        "Estimated travel time",
        format_travel_time(route.distance_km, speed) if route else "—",
        border=True,
    )

left, right = st.columns([1.5, 1], gap="large")
with left:
    with st.container(border=True):
        st.subheader("Quick route summary")
        if route:
            st.markdown("  →  ".join(route.locations))
            st.caption(
                f"{route.start} to {route.destination} · "
                f"{len(route.locations) - 1} road segments"
            )
        else:
            st.info("Optimize the saved delivery plan to see its route summary.")

with right:
    with st.container(border=True):
        st.subheader("Delivery plan")
        request = st.session_state.route_request
        st.markdown(f"**Starting point**  \n{request['start']}")
        if request["delivery_points"]:
            st.markdown("**Delivery locations**")
            for location in request["delivery_points"]:
                st.markdown(f"- {location}")
        else:
            st.markdown("**Delivery locations**  \nNo intermediate stops")
        st.markdown(f"**Destination**  \n{request['destination']}")

st.page_link(
    "app_pages/planner.py",
    label="Edit delivery plan",
    icon=":material/tune:",
    width="stretch",
)
if route:
    st.caption(
        f"Time estimate uses an average speed of {speed} km/h; stops and traffic are not included."
    )
