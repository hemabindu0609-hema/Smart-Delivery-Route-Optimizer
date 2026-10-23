"""Interactive PyDeck map for sample delivery routes."""

from __future__ import annotations

import pydeck as pdk
import streamlit as st

from delivery_routes import Coordinates, DeliveryRoute


def show_delivery_map(
    coordinates: Coordinates,
    route: DeliveryRoute,
    *,
    start: str,
    destination: str,
    delivery_points: tuple[str, ...],
    key: str,
) -> None:
    """Render map markers and a highlighted route line."""
    if not route.locations:
        st.info("Calculate a route to see it on the map.")
        return

    marker_data = []
    stops = set(delivery_points)
    for name, point in coordinates.items():
        if name == start:
            role, color = "Start", [33, 161, 121, 230]
        elif name == destination:
            role, color = "Destination", [239, 107, 91, 230]
        elif name in stops:
            role, color = "Delivery point", [245, 166, 35, 230]
        else:
            role, color = "Location", [112, 142, 181, 190]
        marker_data.append(
            {
                "name": name,
                "role": role,
                "color": color,
                "position": [point["longitude"], point["latitude"]],
            }
        )

    route_coordinates = [
        [coordinates[name]["longitude"], coordinates[name]["latitude"]]
        for name in route.locations
    ]
    route_center = [
        sum(point[0] for point in route_coordinates) / len(route_coordinates),
        sum(point[1] for point in route_coordinates) / len(route_coordinates),
    ]
    layer = pdk.Layer(
        "PathLayer",
        data=[{"path": route_coordinates}],
        get_path="path",
        get_color=[47, 111, 237, 220],
        get_width=7,
        width_min_pixels=4,
        pickable=True,
    )
    markers = pdk.Layer(
        "ScatterplotLayer",
        data=marker_data,
        get_position="position",
        get_fill_color="color",
        get_line_color=[255, 255, 255, 255],
        get_radius=110,
        radius_min_pixels=8,
        line_width_min_pixels=2,
        stroked=True,
        pickable=True,
    )
    deck = pdk.Deck(
        layers=[layer, markers],
        initial_view_state=pdk.ViewState(
            longitude=route_center[0],
            latitude=route_center[1],
            zoom=10,
            pitch=0,
        ),
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        tooltip={"text": "{name}\n{role}"},
    )
    st.pydeck_chart(deck, height=460, key=key)
