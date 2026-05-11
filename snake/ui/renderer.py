from __future__ import annotations

import pygame

from snake import config
from snake.core.enums import Direction
from snake.core.food import Food
from snake.core.game import Game
from snake.core.snake import Cell

_CORNER_SPRITES: dict[frozenset[Direction], str] = {
    frozenset({Direction.UP, Direction.LEFT}): "body_topleft",
    frozenset({Direction.UP, Direction.RIGHT}): "body_topright",
    frozenset({Direction.DOWN, Direction.LEFT}): "body_bottomleft",
    frozenset({Direction.DOWN, Direction.RIGHT}): "body_bottomright",
}

_HEAD_NAMES = {
    Direction.UP: "head_up",
    Direction.DOWN: "head_down",
    Direction.LEFT: "head_left",
    Direction.RIGHT: "head_right",
}
_TAIL_NAMES = {
    Direction.UP: "tail_up",
    Direction.DOWN: "tail_down",
    Direction.LEFT: "tail_left",
    Direction.RIGHT: "tail_right",
}


class Renderer:
    def __init__(self) -> None:
        self.title_font = pygame.font.Font(None, 72)
        self.large_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self._sprites: dict[str, pygame.Surface] = _load_sprites_scaled()

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
        for gx in range(config.GRID_SIZE):
            for gy in range(config.GRID_SIZE):
                shade = config.CELL_SHADE_A if (gx + gy) % 2 == 0 else config.CELL_SHADE_B
                r = pygame.Rect(
                    gx * config.CELL_SIZE,
                    gy * config.CELL_SIZE,
                    config.CELL_SIZE,
                    config.CELL_SIZE,
                ).inflate(-1, -1)
                pygame.draw.rect(surface, shade, r, border_radius=6)
        for x in range(0, config.WINDOW_SIZE + 1, config.CELL_SIZE):
            pygame.draw.line(surface, config.GRID_COLOR, (x, 0), (x, config.WINDOW_SIZE))
        for y in range(0, config.WINDOW_SIZE + 1, config.CELL_SIZE):
            pygame.draw.line(surface, config.GRID_COLOR, (0, y), (config.WINDOW_SIZE, y))

    def draw_snake(self, surface: pygame.Surface, body: list[Cell]) -> None:
        if not body:
            return
        self._draw_head(surface, body)
        self._draw_body(surface, body)
        self._draw_tail(surface, body)

    def _draw_head(self, surface: pygame.Surface, body: list[Cell]) -> None:
        rect = _cell_rect(body[0])
        if len(body) >= 2:
            d = _direction(body[0][0] - body[1][0], body[0][1] - body[1][1])
            name = _HEAD_NAMES.get(d)
            if name and (img := self._sprites.get(name)) is not None:
                surface.blit(img, rect)
                return
        self._fallback_head(surface, rect)

    def _draw_tail(self, surface: pygame.Surface, body: list[Cell]) -> None:
        if len(body) < 2:
            r = _cell_rect(body[-1]).inflate(-4, -4)
            pygame.draw.rect(surface, config.ACCENT_DARK_COLOR, r, border_radius=8)
            return
        rect = _cell_rect(body[-1])
        d = _direction(body[-1][0] - body[-2][0], body[-1][1] - body[-2][1])
        name = _TAIL_NAMES.get(d)
        if name and (img := self._sprites.get(name)) is not None:
            surface.blit(img, rect)
            return
        r = rect.inflate(-4, -4)
        pygame.draw.rect(surface, config.ACCENT_DARK_COLOR, r, border_radius=8)

    def _draw_body(self, surface: pygame.Surface, body: list[Cell]) -> None:
        for i in range(1, len(body) - 1):
            rect = _cell_rect(body[i])
            prev = body[i - 1]
            cur = body[i]
            nxt = body[i + 1]
            dh = _direction(prev[0] - cur[0], prev[1] - cur[1])
            dt = _direction(nxt[0] - cur[0], nxt[1] - cur[1])
            if dh == dt.opposite():
                if dh in {Direction.LEFT, Direction.RIGHT}:
                    name = "body_horizontal"
                else:
                    name = "body_vertical"
                if (img := self._sprites.get(name)) is not None:
                    surface.blit(img, rect)
                else:
                    pygame.draw.rect(
                        surface, config.ACCENT_DARK_COLOR, rect.inflate(-4, -4), border_radius=8
                    )
                continue
            stem = _CORNER_SPRITES.get(frozenset({dh, dt}))
            if stem and (img := self._sprites.get(stem)) is not None:
                surface.blit(img, rect)
            else:
                pygame.draw.rect(
                    surface, config.ACCENT_DARK_COLOR, rect.inflate(-4, -4), border_radius=8
                )

    def draw_food(self, surface: pygame.Surface, food: Food) -> None:
        rect = _cell_rect(food.position)
        if (img := self._sprites.get("apple")) is not None:
            surface.blit(img, rect)
            return
        rr = rect.inflate(-8, -8)
        pygame.draw.ellipse(surface, config.FOOD_COLOR, rr)

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

    def _fallback_head(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        rr = rect.inflate(-4, -4)
        pygame.draw.rect(surface, config.ACCENT_COLOR, rr, border_radius=8)
        pygame.draw.rect(surface, (196, 255, 201), rr, width=2, border_radius=8)


def _cell_rect(cell: Cell) -> pygame.Rect:
    x, y = cell
    return pygame.Rect(
        x * config.CELL_SIZE,
        y * config.CELL_SIZE,
        config.CELL_SIZE,
        config.CELL_SIZE,
    )


def _direction(dx: int, dy: int) -> Direction:
    if dx > 0:
        return Direction.RIGHT
    if dx < 0:
        return Direction.LEFT
    if dy > 0:
        return Direction.DOWN
    return Direction.UP


def _load_sprites_scaled() -> dict[str, pygame.Surface]:
    root = config.asset_dir() / "sprites"
    if not root.is_dir():
        return {}
    size = config.CELL_SIZE
    out: dict[str, pygame.Surface] = {}
    for path in sorted(root.glob("*.png")):
        try:
            raw = pygame.image.load(path).convert_alpha()
            out[path.stem] = pygame.transform.smoothscale(raw, (size, size))
        except pygame.error:
            continue
    return out
