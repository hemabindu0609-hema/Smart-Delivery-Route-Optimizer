"""Calculate the shortest delivery route with Dijkstra's algorithm."""

import streamlit as st

from delivery_routes import load_sample_network, plan_route

graph, _ = load_sample_network()
request = st.session_state.route_request

st.title("Route optimization")
st.write(
    "Calculate the shortest route through the saved delivery plan using "
    "Dijkstra's algorithm."
)

with st.container(border=True):
    st.markdown(
        "**Route to optimize**  \n"
        + "  →  ".join(
            [
                request["start"],
                *request["delivery_points"],
                request["destination"],
            ]
        )
    )

if st.button(
    "Calculate shortest route",
    type="primary",
    icon=":material/bolt:",
    width="stretch",
):
    try:
        optimized_route = plan_route(
            graph,
            request["start"],
            request["destination"],
            request["delivery_points"],
        )
    except ValueError as error:
        st.session_state.optimized_route = None
        st.error(str(error))
    else:
        st.session_state.optimized_route = optimized_route
        st.success("Shortest route calculated with Dijkstra's algorithm.")

route = st.session_state.optimized_route
if route is not None:
    st.metric("Optimized distance", f"{route.distance_km:.1f} km", border=True)
    st.markdown("  →  ".join(route.locations))
    st.page_link(
        "app_pages/route_map.py",
        label="View optimized route map",
        icon=":material/map:",
    )
    st.page_link(
        "app_pages/results.py",
        label="View route results",
        icon=":material/analytics:",
    )
else:
    st.info("Calculate the route to view its map and step-by-step results.")
