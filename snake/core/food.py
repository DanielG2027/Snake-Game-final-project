from __future__ import annotations

import random
from dataclasses import dataclass

from snake.core.snake import Cell


@dataclass(frozen=True)
class Food:
    position: Cell


def spawn_food(
    occupied: set[Cell],
    grid_width: int,
    grid_height: int,
    rng: random.Random | None = None,
) -> Food | None:
    rng = rng or random.Random()
    empty = [
        (x, y)
        for y in range(grid_height)
        for x in range(grid_width)
        if (x, y) not in occupied
    ]
    if not empty:
        return None
    return Food(position=rng.choice(empty))
