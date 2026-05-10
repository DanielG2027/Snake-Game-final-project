from __future__ import annotations

from dataclasses import dataclass

from snake.core.enums import Direction

Cell = tuple[int, int]


@dataclass
class Snake:
    body: list[Cell]
    direction: Direction = Direction.RIGHT
    pending_direction: Direction = Direction.RIGHT

    @classmethod
    def centered(cls, grid_width: int, grid_height: int, length: int = 3) -> Snake:
        center_x = grid_width // 2
        center_y = grid_height // 2
        body = [(center_x - offset, center_y) for offset in range(length)]
        return cls(body=body)

    @property
    def head(self) -> Cell:
        return self.body[0]

    def change_direction(self, direction: Direction) -> bool:
        if direction == self.direction.opposite():
            return False
        self.pending_direction = direction
        return True

    def next_head(self) -> Cell:
        dx, dy = self.pending_direction.vector
        x, y = self.head
        return x + dx, y + dy

    def move(self, *, grow: bool = False) -> Cell:
        self.direction = self.pending_direction
        new_head = self.next_head()
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()
        return new_head

    def collides_with_self(self) -> bool:
        return self.head in self.body[1:]

    def occupies(self) -> set[Cell]:
        return set(self.body)
