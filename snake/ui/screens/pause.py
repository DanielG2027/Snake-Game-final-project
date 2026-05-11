from __future__ import annotations

import pygame

from snake import config
from snake.ui.screen import Screen
from snake.ui.widgets import Button, ButtonGroup


class PauseScreen(Screen):
    def __init__(self, app, play) -> None:
        super().__init__(app)
        self.play = play
        self.buttons = ButtonGroup(
            [
                Button(pygame.Rect(200, 246, 200, 52), "Resume", self._resume),
                Button(pygame.Rect(200, 314, 200, 52), "Main Menu", self.app.show_menu),
                Button(pygame.Rect(200, 382, 200, 52), "Quit", self.app.quit),
            ]
        )

    def _resume(self) -> None:
        self.play.game.resume()
        self.app.screen = self.play

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._resume()
            return
        self.buttons.handle_event(event)

    def draw(self, surface: pygame.Surface) -> None:
        self.play.draw(surface)
        overlay = pygame.Surface((config.WINDOW_SIZE, config.WINDOW_SIZE), pygame.SRCALPHA)
        overlay.fill(config.OVERLAY_COLOR)
        surface.blit(overlay, (0, 0))
        r = self.app.renderer
        r.draw_text(surface, "Paused", (config.WINDOW_SIZE // 2, 170), r.large_font)
        self.buttons.draw(surface, r.font)

