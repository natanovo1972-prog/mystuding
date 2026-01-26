from src.masks import get_mask_card_number, get_mask_account
import pytest


def test_mask_card_number():
    """Тестирование правильности маскирования номера карты со стандартным 16-м номером"""
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


def test_mask_card_number_incorrect():
    """Проверка работы функции на различных форматах номеров карт, включая граничные случаи
    и нестандартрные длины номеров карт"""
    with pytest.raises(ValueError, match="Номер должен содержать 16 цифр") as exc_info:
        get_mask_card_number("700079228960") #Тестируем короткий номер

    with pytest.raises(ValueError, match="Номер должен содержать 16 цифр") as exc_info:
        get_mask_card_number("700007922896063636") #Тестируем длинный номер


def test_mask_card_number_empty():
    """Проверка, что функция корректно обрабатывает строки, где отсутствует номер карты"""
    with pytest.raises(ValueError, match="Номер должен содержать 16 цифр"):
        get_mask_card_number("") #Тестируем пустую строку


def test_mask_account():
    """Проверка правильности маскирования номера счета"""
    assert get_mask_account("73654108430135874305") == "**4305"


def test_mask_account_format_length():
    """Проверка работы функции с различными форматами и длинами номера счета"""
    with pytest.raises(ValueError, match="Номер счета должен содержать 20 цифр") as exc_info:
        get_mask_account("7365 4108 4301 3587 4305") #Тестируем номер с пробелами

    with pytest.raises(ValueError, match="Номер счета должен содержать 20 цифр") as exc_info:
        get_mask_account("736541084301358743005") #Тестируем длинный номер

    with pytest.raises(ValueError, match="Номер счета должен содержать 20 цифр") as exc_info:
        get_mask_account("7365410843013587") #Тестируем короткий номер

