from __future__ import annotations

import pygame

from snake import config
from snake.core.food import Food
from snake.core.game import Game
from snake.core.snake import Cell


class Renderer:
    def __init__(self) -> None:
        self.title_font = pygame.font.Font(None, 72)
        self.large_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)

    def draw_text(
        self,
        surface: pygame.Surface,
        text: str,
        pos: tuple[int, int],
        font: pygame.font.Font,
        color: tuple[int, int, int] = config.TEXT_COLOR,
        align: str = "center",
    ) -> None:
        img = font.render(text, True, color)
        rect = img.get_rect()
        setattr(rect, align, pos)
        surface.blit(img, rect)

    def draw_play(self, surface: pygame.Surface, game: Game, high_score: int) -> None:
        self.draw_board(surface)
        if game.food is not None:
            self.draw_food(surface, game.food)
        self.draw_snake(surface, game.snake.body)
        self.draw_hud(surface, game.score, max(high_score, game.score))

    def draw_board(self, surface: pygame.Surface) -> None:
        surface.fill(config.BACKGROUND_COLOR)
        for x in range(0, config.WINDOW_SIZE, config.CELL_SIZE):
            pygame.draw.line(surface, config.GRID_COLOR, (x, 0), (x, config.WINDOW_SIZE))
        for y in range(0, config.WINDOW_SIZE, config.CELL_SIZE):
            pygame.draw.line(surface, config.GRID_COLOR, (0, y), (config.WINDOW_SIZE, y))

    def draw_snake(self, surface: pygame.Surface, body: list[Cell]) -> None:
        for i, cell in enumerate(body):
            rect = _cell_rect(cell).inflate(-4, -4)
            fill = config.ACCENT_COLOR if i == 0 else config.ACCENT_DARK_COLOR
            pygame.draw.rect(surface, fill, rect, border_radius=8)
            if i == 0:
                pygame.draw.rect(surface, (196, 255, 201), rect, width=2, border_radius=8)

    def draw_food(self, surface: pygame.Surface, food: Food) -> None:
        rect = _cell_rect(food.position).inflate(-8, -8)
        pygame.draw.ellipse(surface, config.FOOD_COLOR, rect)

    def draw_hud(self, surface: pygame.Surface, score: int, high_score: int) -> None:
        self.draw_text(
            surface,
            f"Score: {score}",
            (16, 12),
            self.small_font,
            align="topleft",
        )
        self.draw_text(
            surface,
            f"High: {high_score}",
            (config.WINDOW_SIZE - 16, 12),
            self.small_font,
            align="topright",
        )


def _cell_rect(cell: Cell) -> pygame.Rect:
    x, y = cell
    return pygame.Rect(
        x * config.CELL_SIZE,
        y * config.CELL_SIZE,
        config.CELL_SIZE,
        config.CELL_SIZE,
    )
