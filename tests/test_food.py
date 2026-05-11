import random

from snake.core.food import Food, spawn_food


def test_spawn_returns_food_position_not_in_occupied_when_room_exists() -> None:
    rng = random.Random(0)
    occupied = {(0, 0), (1, 0)}

    food = spawn_food(occupied, 5, 5, rng)

    assert food is not None
    assert isinstance(food, Food)
    assert food.position not in occupied


def test_spawn_returns_none_when_grid_full() -> None:
    occupied = {(x, y) for y in range(2) for x in range(2)}

    food = spawn_food(occupied, 2, 2, random.Random(0))

    assert food is None
