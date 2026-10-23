import unittest

from algorithms.binary_search import binary_search
from algorithms.coin_change import coin_change
from algorithms.merge_sort import merge_sort


class SortingSearchingTests(unittest.TestCase):
    def test_merge_sort_orders_without_mutating_input(self) -> None:
        original = [7, 2, 5, 2, -1]
        self.assertEqual(merge_sort(original), [-1, 2, 2, 5, 7])
        self.assertEqual(original, [7, 2, 5, 2, -1])
        self.assertEqual(merge_sort([]), [])

    def test_binary_search_finds_and_misses(self) -> None:
        values = [-1, 2, 2, 5, 7]
        self.assertIn(binary_search(values, 2), (1, 2))
        self.assertEqual(binary_search(values, 4), -1)
        self.assertEqual(binary_search([], 4), -1)

    def test_coin_change_minimum_and_unreachable_amount(self) -> None:
        self.assertEqual(coin_change([1, 5, 10, 25], 63), (6, [1, 1, 1, 10, 25, 25]))
        self.assertEqual(coin_change([4, 6], 5), (None, []))

    def test_coin_change_validates_input(self) -> None:
        for coins, amount in (([0, 1], 4), ([2], -1), ([], 5), ([1.5], 5)):
            with self.subTest(coins=coins, amount=amount):
                with self.assertRaises(ValueError):
                    coin_change(coins, amount)


if __name__ == "__main__":
    unittest.main()
