from src.decorators import log
from typing import Any


def test_log_success(capsys: Any) -> None:
    @log()
    def add(a: int, b: int) -> int:
        return a + b

    add(1, 2)
    captured = capsys.readouterr()
    assert "add finished" in captured.out
    assert "error" not in captured.out


def test_log_error(capsys: Any) -> None:
    @log()
    def divide(a: int, b: int) -> int:
        return a // b

    divide(5, 0)
    captured = capsys.readouterr()
    assert "divide raised with arguments" in captured.out
    assert "division by zero" in captured.out
    assert "divide finished with error" in captured.out
