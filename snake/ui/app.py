from __future__ import annotations

import pygame

from snake import config
from snake.core.enums import Direction
from snake.core.game import Game
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


def run() -> None:
    pygame.init()
    surface = pygame.display.set_mode((config.WINDOW_SIZE, config.WINDOW_SIZE))
    pygame.display.set_caption(config.TITLE)
    clock = pygame.time.Clock()
    renderer = Renderer()
    game = Game()
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
                        game.change_direction(direction)

        accumulator += dt
        while accumulator >= config.LOGIC_STEP_SECONDS and not game.is_game_over:
            accumulator -= config.LOGIC_STEP_SECONDS
            game.step()

        renderer.draw_board(surface)
        if game.food is not None:
            renderer.draw_food(surface, game.food)
        renderer.draw_snake(surface, game.snake.body)
        renderer.draw_score(surface, game.score)
        pygame.display.flip()

    pygame.quit()
