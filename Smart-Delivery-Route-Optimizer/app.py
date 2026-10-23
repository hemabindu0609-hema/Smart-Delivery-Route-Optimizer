"""Streamlit entry point for Smart Delivery Route Optimizer."""

from __future__ import annotations

import streamlit as st

from delivery_routes import load_sample_network, plan_route


def initialize_state() -> None:
    graph, _ = load_sample_network()
    if "average_speed" not in st.session_state:
        st.session_state.average_speed = 30
    default_request = {
        "start": "Shindevasti",
        "destination": "Pheonix Millenium Mall Wakad",
        "delivery_points": ["Alard Univercity"],
    }
    request = st.session_state.get("route_request")
    valid_locations = set(graph)
    request_locations = (
        [request["start"], request["destination"], *request["delivery_points"]]
        if request is not None
        else []
    )
    if request is None or not set(request_locations).issubset(valid_locations):
        st.session_state.route_request = {
            **default_request,
        }
        st.session_state.optimized_route = None
    if st.session_state.get("optimized_route") is None:
        request = st.session_state.route_request
        st.session_state.optimized_route = plan_route(
            graph,
            request["start"],
            request["destination"],
            request["delivery_points"],
        )


def main() -> None:
    st.set_page_config(
        page_title="Smart Delivery Route Optimizer",
        page_icon=":material/local_shipping:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    initialize_state()

    with st.sidebar:
        st.markdown("## :material/local_shipping: Route optimizer")
        st.caption("Smarter routes. Simpler deliveries.")
        st.slider(
            "Average delivery speed (km/h)",
            min_value=10,
            max_value=80,
            step=5,
            key="average_speed",
            help="Used to estimate travel time; it is not a live traffic estimate.",
        )
        st.caption("Sample road distances and map coordinates are illustrative.")

    page = st.navigation(
        {
            "Route planning": [
                st.Page(
                    "app_pages/dashboard.py",
                    title="Dashboard",
                    icon=":material/dashboard:",
                    default=True,
                ),
                st.Page(
                    "app_pages/planner.py",
                    title="Route Planner",
                    icon=":material/tune:",
                ),
                st.Page(
                    "app_pages/optimization.py",
                    title="Route Optimization",
                    icon=":material/route:",
                ),
                st.Page(
                    "app_pages/route_map.py",
                    title="Route Map",
                    icon=":material/map:",
                ),
                st.Page(
                    "app_pages/results.py",
                    title="Results",
                    icon=":material/analytics:",
                ),
            ]
        },
        position="sidebar",
    )
    page.run()


if __name__ == "__main__":
    main()
