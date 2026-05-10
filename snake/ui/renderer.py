from __future__ import annotations

import pygame

from snake import config
from snake.core.snake import Cell


class Renderer:
    def draw_board(self, surface: pygame.Surface) -> None:
        surface.fill(config.BACKGROUND_COLOR)
        for x in range(0, config.WINDOW_SIZE, config.CELL_SIZE):
            pygame.draw.line(surface, config.GRID_COLOR, (x, 0), (x, config.WINDOW_SIZE))
        for y in range(0, config.WINDOW_SIZE, config.CELL_SIZE):
            pygame.draw.line(surface, config.GRID_COLOR, (0, y), (config.WINDOW_SIZE, y))

    def draw_snake(self, surface: pygame.Surface, body: list[Cell]) -> None:
        for index, cell in enumerate(body):
            rect = self._cell_rect(cell).inflate(-4, -4)
            color = config.ACCENT_COLOR if index == 0 else config.ACCENT_DARK_COLOR
            pygame.draw.rect(surface, color, rect, border_radius=8)
            if index == 0:
                pygame.draw.rect(surface, (196, 255, 201), rect, width=2, border_radius=8)

    @staticmethod
    def _cell_rect(cell: Cell) -> pygame.Rect:
        x, y = cell
        return pygame.Rect(
            x * config.CELL_SIZE,
            y * config.CELL_SIZE,
            config.CELL_SIZE,
            config.CELL_SIZE,
        )
