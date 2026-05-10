from __future__ import annotations

from enum import Enum, auto


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def vector(self) -> tuple[int, int]:
        return self.value

    def opposite(self) -> Direction:
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return opposites[self]


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
