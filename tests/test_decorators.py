import pytest
from src.decorators import log, my_function


def test_log_success(capsys):
    @log()
    def add(a, b) -> Any:
        return a + b

    add(1, 2)
    captured = capsys.readouterr()
    assert "my_function finished" in captured.out