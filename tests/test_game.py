import random

from snake.core.food import Food
from snake.core.game import Game


def test_eating_grows_snake_updates_score_respawns_food_off_snake() -> None:
    game = Game(rng=random.Random(1))
    game.food = Food((11, 10))

    result = game.step()

    assert result.ate_food is True
    assert game.score == 1
    assert len(game.snake.body) == 4
    assert game.food is not None
    assert game.food.position not in game.snake.occupies()
