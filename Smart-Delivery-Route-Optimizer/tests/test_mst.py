import unittest

from algorithms.kruskal import kruskal_mst
from algorithms.prim import prim_mst


class MinimumSpanningTreeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = {
            "A": {"B": 4, "C": 3},
            "B": {"A": 4, "C": 1, "D": 2},
            "C": {"A": 3, "B": 1, "D": 4},
            "D": {"B": 2, "C": 4},
        }

    def test_prim_and_kruskal_return_minimum_tree(self) -> None:
        for algorithm in (prim_mst, kruskal_mst):
            edges, total, connected = algorithm(self.graph)
            self.assertTrue(connected)
            self.assertEqual(len(edges), 3)
            self.assertEqual(total, 6.0)

    def test_disconnected_graph_returns_forest(self) -> None:
        graph = {"A": {"B": 2}, "B": {"A": 2}, "C": {}}
        for algorithm in (prim_mst, kruskal_mst):
            edges, total, connected = algorithm(graph)
            self.assertEqual(edges, [("A", "B", 2.0)])
            self.assertEqual(total, 2.0)
            self.assertFalse(connected)

    def test_mst_rejects_asymmetric_input(self) -> None:
        with self.assertRaises(ValueError):
            prim_mst({"A": {"B": 2}, "B": {}})


if __name__ == "__main__":
    unittest.main()
