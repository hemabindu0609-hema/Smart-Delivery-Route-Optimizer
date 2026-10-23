"""Dynamic programming solution to the unbounded minimum coin-change problem."""

from __future__ import annotations

from collections.abc import Iterable


def coin_change(coins: Iterable[int], amount: int) -> tuple[int | None, list[int]]:
    """Return the minimum coin count and one solution, or ``(None, [])``.

    Denominations must be positive integers and ``amount`` must be a
    non-negative integer. Each denomination can be used any number of times.
    """
    if isinstance(amount, bool) or not isinstance(amount, int) or amount < 0:
        raise ValueError("Amount must be a non-negative integer.")
    denominations = list(coins)
    if not denominations:
        raise ValueError("Provide at least one coin denomination.")
    if any(
        isinstance(coin, bool) or not isinstance(coin, int) or coin <= 0
        for coin in denominations
    ):
        raise ValueError("Coin denominations must be positive integers.")
    denominations = sorted(set(denominations))

    best = [amount + 1] * (amount + 1)
    last_coin = [0] * (amount + 1)
    best[0] = 0
    for value in range(1, amount + 1):
        for coin in denominations:
            if coin > value:
                break
            if best[value - coin] + 1 < best[value]:
                best[value] = best[value - coin] + 1
                last_coin[value] = coin

    if best[amount] > amount:
        return None, []
    solution: list[int] = []
    remaining = amount
    while remaining:
        coin = last_coin[remaining]
        solution.append(coin)
        remaining -= coin
    return best[amount], solution
