from __future__ import annotations

import sys
from pathlib import Path

WINDOW_SIZE = 600
GRID_SIZE = 20
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
RENDER_FPS = 60
LOGIC_FPS = 10
LOGIC_STEP_SECONDS = 1 / LOGIC_FPS

TITLE = "Snake"
SCORES_DB_NAME = "scores.db"
SETTINGS_NAME = "settings.json"

BACKGROUND_COLOR = (18, 24, 38)
CELL_SHADE_A = (22, 30, 44)
CELL_SHADE_B = (16, 22, 36)
GRID_COLOR = (28, 36, 54)
PANEL_COLOR = (24, 31, 48)
TEXT_COLOR = (232, 238, 247)
MUTED_TEXT_COLOR = (153, 166, 190)
ACCENT_COLOR = (118, 222, 128)
ACCENT_DARK_COLOR = (64, 160, 82)
FOOD_COLOR = (236, 87, 87)
BUTTON_COLOR = (42, 54, 80)
BUTTON_HOVER_COLOR = (58, 75, 110)
BUTTON_FOCUS_COLOR = (89, 116, 168)
OVERLAY_COLOR = (0, 0, 0, 170)


def runtime_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path.cwd()


def runtime_path(filename: str) -> Path:
    return runtime_dir() / filename


def asset_dir() -> Path:
    base = getattr(sys, "_MEIPASS", None)
    if isinstance(base, str):
        return Path(base) / "snake" / "assets"
    return Path(__file__).resolve().parent / "assets"
