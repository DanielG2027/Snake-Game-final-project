from __future__ import annotations

import pygame

from snake import config


def run() -> None:
    pygame.init()
    surface = pygame.display.set_mode((config.WINDOW_SIZE, config.WINDOW_SIZE))
    pygame.display.set_caption(config.TITLE)
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(config.RENDER_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        surface.fill(config.BACKGROUND_COLOR)
        pygame.display.flip()

    pygame.quit()
