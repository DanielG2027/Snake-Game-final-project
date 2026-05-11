from __future__ import annotations

import random
from dataclasses import dataclass, field

from snake.config import GRID_SIZE
from snake.core.enums import Direction
from snake.core.food import Food, spawn_food
from snake.core.snake import Snake


@dataclass(frozen=True)
class StepResult:
    ate_food: bool = False


def _in_bounds(cell: tuple[int, int], width: int, height: int) -> bool:
    x, y = cell
    return 0 <= x < width and 0 <= y < height


@dataclass
class Game:
    grid_width: int = GRID_SIZE
    grid_height: int = GRID_SIZE
    rng: random.Random = field(default_factory=random.Random)
    snake: Snake = field(init=False)
    food: Food | None = field(init=False, default=None)
    score: int = field(init=False, default=0)

    def __post_init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.snake = Snake.centered(self.grid_width, self.grid_height)
        self.score = 0
        self.food = spawn_food(
            self.snake.occupies(), self.grid_width, self.grid_height, self.rng
        )

    def change_direction(self, direction: Direction) -> bool:
        return self.snake.change_direction(direction)

    def step(self) -> StepResult:
        nxt = self.snake.next_head()
        if not _in_bounds(nxt, self.grid_width, self.grid_height):
            return StepResult()

        eating = self.food is not None and nxt == self.food.position
        self.snake.move(grow=eating)
        if eating:
            self.score += 1
            self.food = spawn_food(
                self.snake.occupies(),
                self.grid_width,
                self.grid_height,
                self.rng,
            )
            return StepResult(ate_food=True)
        return StepResult()
