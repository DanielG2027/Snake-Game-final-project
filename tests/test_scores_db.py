import pytest

from snake.db.scores import ScoresRepo


def test_add_score_rejects_negative(tmp_path: object) -> None:
    repo = ScoresRepo(tmp_path / "s.db")

    with pytest.raises(ValueError, match=">="):
        repo.add_score(-1)


def test_qualifies_requires_non_negative_score(tmp_path: object) -> None:
    repo = ScoresRepo(tmp_path / "s.db")

    with pytest.raises(ValueError, match=">="):
        repo.qualifies(-5)


def test_qualifies_when_fewer_than_n_entries(tmp_path: object) -> None:
    repo = ScoresRepo(tmp_path / "s.db")
    repo.add_score(10)
    repo.add_score(3)

    assert repo.qualifies(0, n=10) is True


def test_qualifies_when_score_meets_nth_best(tmp_path: object) -> None:
    repo = ScoresRepo(tmp_path / "s.db")
    for s in range(90, 100):
        repo.add_score(s)

    assert repo.qualifies(93, n=10) is True


def test_qualifies_false_when_below_nth_best(tmp_path: object) -> None:
    repo = ScoresRepo(tmp_path / "s.db")
    for s in range(90, 100):
        repo.add_score(s)

    assert repo.qualifies(88, n=10) is False


def test_best_score_empty_is_zero(tmp_path: object) -> None:
    repo = ScoresRepo(tmp_path / "s.db")

    assert repo.best_score() == 0


def test_best_score_reflects_database_max(tmp_path: object) -> None:
    repo = ScoresRepo(tmp_path / "s.db")
    repo.add_score(4)
    repo.add_score(9)

    assert repo.best_score() == 9


def test_top_n_orders_by_score_then_id(tmp_path: object) -> None:
    repo = ScoresRepo(tmp_path / "s.db")
    repo.add_score(50)
    repo.add_score(100)
    repo.add_score(50)

    rows = repo.top_n(2)

    assert [r.score for r in rows] == [100, 50]
