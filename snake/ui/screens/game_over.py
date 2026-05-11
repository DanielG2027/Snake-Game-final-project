from __future__ import annotations

import pygame

from snake import config
from snake.ui.screen import Screen
from snake.ui.widgets import Button, ButtonGroup


class GameOverScreen(Screen):
    def __init__(self, app, score: int) -> None:
        super().__init__(app)
        self.score = score
        self.buttons = ButtonGroup(
            [
                Button(pygame.Rect(200, 290, 200, 52), "Try Again", self.app.start_game),
                Button(pygame.Rect(200, 358, 200, 52), "Main Menu", self.app.show_menu),
                Button(pygame.Rect(200, 426, 200, 52), "Quit", self.app.quit),
            ]
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.show_menu()
            return
        self.buttons.handle_event(event)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(config.BACKGROUND_COLOR)
        r = self.app.renderer
        r.draw_text(
            surface,
            "Game Over",
            (config.WINDOW_SIZE // 2, 124),
            r.large_font,
            config.FOOD_COLOR,
        )
        r.draw_text(surface, f"{self.score}", (config.WINDOW_SIZE // 2, 204), r.font)
        self.buttons.draw(surface, r.font)

