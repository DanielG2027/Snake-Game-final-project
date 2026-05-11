from __future__ import annotations

import pygame

from snake import config
from snake.ui.screen import Screen
from snake.ui.widgets import Button, ButtonGroup


class MenuScreen(Screen):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.buttons = ButtonGroup(
            [
                Button(pygame.Rect(200, 250, 200, 52), "Play", self.app.start_game),
                Button(pygame.Rect(200, 318, 200, 52), "Quit", self.app.quit),
            ]
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.app.start_game()
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.quit()
            return
        self.buttons.handle_event(event)

    def draw(self, surface: pygame.Surface) -> None:
        r = self.app.renderer
        surface.fill(config.BACKGROUND_COLOR)
        r.draw_text(
            surface,
            config.TITLE,
            (config.WINDOW_SIZE // 2, 110),
            r.title_font,
            config.ACCENT_COLOR,
        )
        r.draw_text(
            surface,
            "Space to play",
            (config.WINDOW_SIZE // 2, 184),
            r.small_font,
            config.MUTED_TEXT_COLOR,
        )
        self.buttons.draw(surface, r.font)

