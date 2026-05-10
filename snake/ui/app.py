from __future__ import annotations

import pygame

from snake import config
from snake.core.enums import Direction
from snake.core.snake import Snake
from snake.ui.renderer import Renderer

KEY_DIRECTIONS = {
    pygame.K_UP: Direction.UP,
    pygame.K_w: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_s: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_a: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT,
    pygame.K_d: Direction.RIGHT,
}


def _in_bounds(cell: tuple[int, int]) -> bool:
    x, y = cell
    return 0 <= x < config.GRID_SIZE and 0 <= y < config.GRID_SIZE


def run() -> None:
    pygame.init()
    surface = pygame.display.set_mode((config.WINDOW_SIZE, config.WINDOW_SIZE))
    pygame.display.set_caption(config.TITLE)
    clock = pygame.time.Clock()
    renderer = Renderer()
    snake = Snake.centered(config.GRID_SIZE, config.GRID_SIZE)
    accumulator = 0.0
    running = True

    while running:
        dt = clock.tick(config.RENDER_FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    direction = KEY_DIRECTIONS.get(event.key)
                    if direction is not None:
                        snake.change_direction(direction)

        accumulator += dt
        while accumulator >= config.LOGIC_STEP_SECONDS:
            accumulator -= config.LOGIC_STEP_SECONDS
            next_cell = snake.next_head()
            if _in_bounds(next_cell):
                snake.move()

        renderer.draw_board(surface)
        renderer.draw_snake(surface, snake.body)
        pygame.display.flip()

    pygame.quit()
