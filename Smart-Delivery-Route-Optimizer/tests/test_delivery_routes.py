import unittest

from delivery_routes import (
    format_travel_time,
    load_sample_network,
    plan_route,
    route_directions,
)


class DeliveryRouteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = {
            "Depot": {"Direct": 100, "West": 1},
            "Direct": {"Depot": 100, "Stop": 1},
            "West": {"Depot": 1, "Bridge": 1},
            "Bridge": {"West": 1, "Stop": 1},
            "Stop": {"Direct": 1, "Bridge": 1, "End": 1},
            "End": {"Stop": 1},
        }

    def test_dijkstra_optimizes_each_ordered_delivery_leg(self) -> None:
        route = plan_route(self.graph, "Depot", "End", ["Stop"])

        self.assertEqual(
            route.locations,
            ("Depot", "West", "Bridge", "Stop", "End"),
        )
        self.assertEqual(route.distance_km, 4.0)
        self.assertEqual(route.start, "Depot")
        self.assertEqual(route.delivery_points, ("Stop",))
        self.assertEqual(route.destination, "End")

    def test_route_directions_include_each_road_distance(self) -> None:
        route = plan_route(self.graph, "Depot", "End", ["Stop"])

        directions = route_directions(self.graph, route.locations)

        self.assertEqual(len(directions), 4)
        self.assertEqual(directions[0]["direction"], "Travel from Depot to West")
        self.assertEqual(directions[0]["distance"], "1.0 km")

    def test_sample_network_has_coordinates_for_every_location(self) -> None:
        graph, coordinates = load_sample_network()

        self.assertEqual(set(graph), set(coordinates))
        self.assertEqual(
            set(graph),
            {
                "Shindevasti",
                "RK PG",
                "NexaUltra Stay PG",
                "Alard Univercity",
                "Cafe De Flora",
                "Jigri Katta",
                "Dmart Hinjewadi",
                "Pheonix Millenium Mall Wakad",
            },
        )
        self.assertTrue(all("latitude" in point and "longitude" in point for point in coordinates.values()))

    def test_sample_route_uses_dijkstra_for_multiple_delivery_legs(self) -> None:
        graph, _ = load_sample_network()

        route = plan_route(
            graph,
            "Shindevasti",
            "Pheonix Millenium Mall Wakad",
            ["Alard Univercity"],
        )

        self.assertAlmostEqual(route.distance_km, 13.8)
        self.assertEqual(
            route.locations,
            (
                "Shindevasti",
                "NexaUltra Stay PG",
                "Alard Univercity",
                "NexaUltra Stay PG",
                "Pheonix Millenium Mall Wakad",
            ),
        )

    def test_invalid_or_duplicate_delivery_points_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot contain duplicates"):
            plan_route(self.graph, "Depot", "End", ["Stop", "Stop"])
        with self.assertRaisesRegex(ValueError, "cannot also be delivery points"):
            plan_route(self.graph, "Depot", "End", ["Depot"])

    def test_travel_time_uses_the_configured_average_speed(self) -> None:
        self.assertEqual(format_travel_time(15, 30), "30 min")
        self.assertEqual(format_travel_time(75, 30), "2 hr 30 min")


if __name__ == "__main__":
    unittest.main()
