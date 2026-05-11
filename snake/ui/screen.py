from __future__ import annotations

import pygame


class Screen:
    def __init__(self, app) -> None:
        self.app = app

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        raise NotImplementedError

