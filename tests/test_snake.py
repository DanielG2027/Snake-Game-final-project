from snake.core.enums import Direction
from snake.core.snake import Snake


def test_change_direction_blocks_opposite() -> None:
    snake = Snake(
        body=[(5, 5), (4, 5), (3, 5)],
        direction=Direction.RIGHT,
        pending_direction=Direction.RIGHT,
    )

    ok = snake.change_direction(Direction.LEFT)

    assert ok is False


def test_move_applies_pending_direction_then_appends_head() -> None:
    snake = Snake(
        body=[(10, 10), (9, 10)],
        direction=Direction.RIGHT,
        pending_direction=Direction.UP,
    )

    snake.move()

    assert snake.direction == Direction.UP
    assert snake.head == (10, 9)
    assert len(snake.body) == 2


def test_collides_with_self_true_when_head_duplicate() -> None:
    snake = Snake(body=[(1, 1), (2, 1)])

    snake.body[0] = (2, 1)

    assert snake.collides_with_self() is True
