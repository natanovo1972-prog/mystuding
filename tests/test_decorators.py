from src.decorators import log
from typing import Any


def test_log_success(capsys: Any) -> None:
    # Тест на успешное выполнение функций (вывод в консоль)
    @log()
    def func_add(a: int, b: int) -> int:
        return a + b

    func_add(1, 2)
    captured = capsys.readouterr()
    assert "func_add finished" in captured.out
    assert "error" not in captured.out


def test_log_error(capsys: Any) -> None:
    # Тест на обработку исключений (вывод в консоль)
    @log()
    def func_divide(a: int, b: int) -> int:
        return a // b

    func_divide(5, 0)
    captured = capsys.readouterr()
    assert "func_divide raised with arguments ((5, 0), {}) but it didn't worked," in captured.out
    assert "func_divide finished with error" in captured.out


@log(filename="my_file.txt")
# Тест на успешное выполнение функции (вывод в файл)
def add(a: int, b: int) -> int:
    return a * b


def test_log_to_file() -> None:
    add(5, 7)
    with open("my_file.txt", "r") as file:
        content = file.read()
    assert "add finished" in content


@log(filename="my_file.txt")
# Тест на обработку исключений (вывод в файл)
def divide(a: int, b: int) -> int:
    return a // b


def test_log_to_file_error() -> None:
    divide(5, 0)
    with open("my_file.txt", "r") as file:
        content = file.read()
    assert "divide finished with error" in content
