from src.decorators import log
from typing import Any
import pytest


def test_log_success(capsys: Any) -> None:
    """Тест на успешное выполнение функций (вывод в консоль)"""
    @log()
    def func_add(a: int, b: int) -> int:
        return a + b

    func_add(1, 2)
    captured = capsys.readouterr()
    assert "func_add finished" in captured.out
    assert "error" not in captured.out


def test_log_error(capsys: Any) -> None:
    """Тест на обработку исключений (вывод в консоль)"""
    @log()
    def func_divide(a: int, b: int) -> int:
        return a // b

    func_divide(5, 0)
    captured = capsys.readouterr()
    assert "func_divide raised with arguments ((5, 0), {}) but it didn't worked," in captured.out
    assert "func_divide finished with error" in captured.out


@log(filename="my_file.txt")
def add(a: int, b: int) -> int:
    return a * b


def test_log_to_file() -> None:
    """Тест на успешное выполнение функции (вывод в файл)"""
    add(5, 7)
    with open("my_file.txt", "r") as file:
        content = file.read()
    assert "add finished" in content


@log(filename="my_file.txt")
def divide(a: int, b: int) -> int:
    return a // b


def test_log_to_file_error() -> None:
    """Тест на обработку исключений (вывод в файл)"""
    divide(5, 0)
    with open("my_file.txt", "r") as file:
        content = file.read()
    assert "divide finished with error" in content


def test_log_correct_value() -> None:
    """Тестируем, что декоратор корректно возвращает значение функции пользователю"""
    @log()
    def multiply(a: int, b: int):
        return a * b

    result = multiply(5, 20)
    assert result == 100


def test_log_way_to_filename_error() -> None:
    """Тестируем ошибочный путь к файлу"""
    way_error = "no exist folder/my_file.txt"

    @log(filename=way_error)
    def way():
        return "hello"
    with pytest.raises(FileNotFoundError):
        way()
