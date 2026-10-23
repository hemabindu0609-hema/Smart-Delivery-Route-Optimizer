import math
import unittest

from algorithms.bellman_ford import bellman_ford
from algorithms.dijkstra import dijkstra


class ShortestPathTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = {
            "A": {"B": 4, "C": 2},
            "B": {"A": 4, "C": 1, "D": 5},
            "C": {"A": 2, "B": 1, "D": 8},
            "D": {"B": 5, "C": 8},
            "Isolated": {},
        }

    def test_dijkstra_finds_shortest_path(self) -> None:
        self.assertEqual(dijkstra(self.graph, "A", "D"), (["A", "C", "B", "D"], 8.0))

    def test_identical_endpoints_return_zero_distance(self) -> None:
        self.assertEqual(dijkstra(self.graph, "A", "A"), (["A"], 0.0))

    def test_unreachable_destination(self) -> None:
        path, distance = dijkstra(self.graph, "A", "Isolated")
        self.assertEqual(path, [])
        self.assertTrue(math.isinf(distance))

    def test_invalid_endpoint_and_negative_weight_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            dijkstra(self.graph, "missing", "A")
        with self.assertRaises(ValueError):
            dijkstra({"A": {"B": -1}, "B": {}}, "A", "B")

    def test_bellman_ford_supports_negative_edges_without_negative_cycle(self) -> None:
        graph = {"A": {"B": 4, "C": 5}, "B": {"C": -2}, "C": {}}
        self.assertEqual(bellman_ford(graph, "A", "C"), (["A", "B", "C"], 2.0))

    def test_bellman_ford_reports_reachable_negative_cycle(self) -> None:
        graph = {"A": {"B": 1}, "B": {"C": -3}, "C": {"B": 1}}
        with self.assertRaisesRegex(ValueError, "negative-weight cycle"):
            bellman_ford(graph, "A", "C")


if __name__ == "__main__":
    unittest.main()
