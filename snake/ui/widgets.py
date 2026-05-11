from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import pygame

from snake import config


@dataclass
class Button:
    rect: pygame.Rect
    text: str
    action: Callable[[], None]
    focused: bool = False
    hovered: bool = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()
                return True
        if event.type == pygame.KEYDOWN and self.focused:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.action()
                return True
        return False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        if self.focused:
            fill = config.BUTTON_FOCUS_COLOR
        elif self.hovered:
            fill = config.BUTTON_HOVER_COLOR
        else:
            fill = config.BUTTON_COLOR

        pygame.draw.rect(surface, fill, self.rect, border_radius=12)
        pygame.draw.rect(
            surface, config.MUTED_TEXT_COLOR, self.rect, width=2, border_radius=12
        )
        label = font.render(self.text, True, config.TEXT_COLOR)
        surface.blit(label, label.get_rect(center=self.rect.center))


class ButtonGroup:
    def __init__(self, buttons: list[Button]) -> None:
        self.buttons = buttons
        self.focus_index = 0
        self._sync()

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.focus_index = (self.focus_index - 1) % len(self.buttons)
                self._sync()
                return True
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.focus_index = (self.focus_index + 1) % len(self.buttons)
                self._sync()
                return True

        for i, btn in enumerate(self.buttons):
            if btn.handle_event(event):
                return True
            if event.type == pygame.MOUSEMOTION and btn.hovered:
                self.focus_index = i
                self._sync()
        return False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        for btn in self.buttons:
            btn.draw(surface, font)

    def _sync(self) -> None:
        for i, btn in enumerate(self.buttons):
            btn.focused = i == self.focus_index

