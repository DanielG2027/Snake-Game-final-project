from __future__ import annotations

import pygame

from snake.config import LOGIC_STEP_SECONDS
from snake.core.game import Game
from snake.ui.keys import KEY_TO_DIRECTION
from snake.ui.screen import Screen


class PlayScreen(Screen):
    def __init__(self, app, game: Game | None = None) -> None:
        super().__init__(app)
        self.game = game or Game()
        self.accumulator = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.game.pause()
            self.app.show_pause(self)
            return
        direction = KEY_TO_DIRECTION.get(event.key)
        if direction is not None:
            self.game.change_direction(direction)

    def update(self, dt: float) -> None:
        self.accumulator += dt
        while self.accumulator >= LOGIC_STEP_SECONDS and not self.game.is_game_over:
            self.accumulator -= LOGIC_STEP_SECONDS
            result = self.game.step()
            if result.game_over:
                self.app.session_best = max(self.app.session_best, self.game.score)
                self.app.show_game_over(self.game.score)
                return

    def draw(self, surface: pygame.Surface) -> None:
        high = max(self.app.session_best, self.game.score)
        self.app.renderer.draw_play(surface, self.game, high)

