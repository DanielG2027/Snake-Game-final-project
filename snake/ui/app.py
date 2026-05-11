from __future__ import annotations

import pygame

from snake import config
from snake.core.game import Game
from snake.db import ScoresRepo
from snake.ui.renderer import Renderer
from snake.ui.screens.game_over import GameOverScreen
from snake.ui.screens.menu import MenuScreen
from snake.ui.screens.pause import PauseScreen
from snake.ui.screens.play import PlayScreen


def run() -> None:
    pygame.init()
    surface = pygame.display.set_mode((config.WINDOW_SIZE, config.WINDOW_SIZE))
    pygame.display.set_caption(config.TITLE)
    clock = pygame.time.Clock()
    renderer = Renderer()

    class App:
        def __init__(self) -> None:
            self.renderer = renderer
            self.session_best = 0
            self.scores = ScoresRepo(config.runtime_path(config.SCORES_DB_NAME))
            self.screen = MenuScreen(self)

        def high_score(self) -> int:
            return max(self.session_best, self.scores.best_score())

        def start_game(self) -> None:
            self.screen = PlayScreen(self, Game())

        def show_menu(self) -> None:
            self.screen = MenuScreen(self)

        def show_pause(self, play: PlayScreen) -> None:
            self.screen = PauseScreen(self, play)

        def show_game_over(self, score: int) -> None:
            self.session_best = max(self.session_best, score)
            self.scores.add_score(score)
            self.screen = GameOverScreen(self, score)

        def quit(self) -> None:
            nonlocal running
            running = False

    running = True
    app = App()

    while running:
        dt = clock.tick(config.RENDER_FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                app.screen.handle_event(event)

        app.screen.update(dt)
        app.screen.draw(surface)
        pygame.display.flip()

    pygame.quit()
