import random

from snake.core.enums import Direction, GameState
from snake.core.food import Food
from snake.core.game import Game
from snake.core.snake import Snake


def test_eating_grows_snake_updates_score_respawns_food_off_snake() -> None:
    game = Game(rng=random.Random(1))
    game.food = Food((11, 10))

    result = game.step()

    assert result.ate_food is True
    assert game.score == 1
    assert len(game.snake.body) == 4
    assert game.food is not None
    assert game.food.position not in game.snake.occupies()


def test_wall_collision_sets_game_over() -> None:
    game = Game()
    game.snake = Snake(body=[(19, 10), (18, 10), (17, 10)])

    result = game.step()

    assert result.game_over is True
    assert game.state == GameState.GAME_OVER


def test_self_collision_sets_game_over() -> None:
    game = Game()
    game.snake = Snake(
        body=[(5, 5), (5, 6), (4, 6), (4, 5), (4, 4), (5, 4)],
        direction=Direction.RIGHT,
        pending_direction=Direction.RIGHT,
    )
    game.change_direction(Direction.DOWN)

    result = game.step()

    assert result.game_over is True
    assert game.state == GameState.GAME_OVER


def test_pause_stops_steps_until_resume() -> None:
    game = Game()
    body_before = list(game.snake.body)

    game.pause()
    game.step()

    assert game.snake.body == body_before
    game.resume()
    game.step()
    assert game.snake.body != body_before


def test_is_game_over_flag() -> None:
    game = Game()
    assert game.is_game_over is False

    game.snake = Snake(body=[(19, 10), (18, 10), (17, 10)])
    game.step()

    assert game.is_game_over is True


def test_pause_blocks_direction_changes() -> None:
    game = Game()
    game.pause()
    ok = game.change_direction(Direction.DOWN)

    assert ok is False
    body_before = list(game.snake.body)
    game.step()
    assert game.snake.body == body_before


def test_reset_clears_score_and_live_state() -> None:
    game = Game(rng=random.Random(0))
    game.food = Food((11, 10))
    game.step()
    score_after = game.score
    length_after = len(game.snake.body)

    game.reset()

    assert game.score == 0
    assert game.state == GameState.PLAYING
    assert len(game.snake.body) == 3
    assert score_after > 0
    assert length_after > len(game.snake.body)
