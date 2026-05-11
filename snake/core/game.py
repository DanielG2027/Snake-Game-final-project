from __future__ import annotations

import random
from dataclasses import dataclass, field

from snake.config import GRID_SIZE
from snake.core.enums import Direction, GameState
from snake.core.food import Food, spawn_food
from snake.core.snake import Snake


@dataclass(frozen=True)
class StepResult:
    ate_food: bool = False
    game_over: bool = False


@dataclass
class Game:
    grid_width: int = GRID_SIZE
    grid_height: int = GRID_SIZE
    rng: random.Random = field(default_factory=random.Random)
    snake: Snake = field(init=False)
    food: Food | None = field(init=False, default=None)
    score: int = field(init=False, default=0)
    state: GameState = field(init=False, default=GameState.PLAYING)

    def __post_init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.snake = Snake.centered(self.grid_width, self.grid_height)
        self.score = 0
        self.state = GameState.PLAYING
        self.food = spawn_food(
            self.snake.occupies(), self.grid_width, self.grid_height, self.rng
        )

    @property
    def is_game_over(self) -> bool:
        return self.state == GameState.GAME_OVER

    def change_direction(self, direction: Direction) -> bool:
        if self.state != GameState.PLAYING:
            return False
        return self.snake.change_direction(direction)

    def pause(self) -> None:
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED

    def resume(self) -> None:
        if self.state == GameState.PAUSED:
            self.state = GameState.PLAYING

    def step(self) -> StepResult:
        if self.state != GameState.PLAYING:
            return StepResult()

        eating = self.food is not None and self.snake.next_head() == self.food.position
        self.snake.move(grow=eating)

        if self._hit_wall() or self.snake.collides_with_self():
            self.state = GameState.GAME_OVER
            return StepResult(game_over=True)

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

    def _hit_wall(self) -> bool:
        x, y = self.snake.head
        return x < 0 or x >= self.grid_width or y < 0 or y >= self.grid_height
