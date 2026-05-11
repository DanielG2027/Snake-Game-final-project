from __future__ import annotations

import pygame

from snake import config
from snake.core.game import Game
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
    screen = MenuScreen(None)

    class App:
        def __init__(self) -> None:
            self.renderer = renderer
            self.screen = screen
            self.session_best = 0

        def start_game(self) -> None:
            self.screen = PlayScreen(self, Game())

        def show_menu(self) -> None:
            self.screen = MenuScreen(self)

        def show_pause(self, play: PlayScreen) -> None:
            self.screen = PauseScreen(self, play)

        def show_game_over(self, score: int) -> None:
            self.screen = GameOverScreen(self, score)

        def quit(self) -> None:
            nonlocal running
            running = False

    running = True
    app = App()
    app.screen = MenuScreen(app)

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
