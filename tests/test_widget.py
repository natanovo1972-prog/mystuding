from src.widget import mask_account_card, get_date
import pytest


@pytest.mark.parametrize("input_number, expected", [
    ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
    ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
    ("Счет 73654108430135874305", "Счет **4305")])
def test_mask_account_card(input_number: str, expected: str):
    """Тестируем, что функция корректно распознает и применяет
    нужный тип маскировки в зависимости от типа входных данных"""
    assert mask_account_card(input_number) == expected


@pytest.mark.parametrize("invalid_number", [
    ("Visa Platinum 89909221136652"),      # Введен короткий номер карты
    ("Счет 736541084301358743"),           # Введен короткий номер счета
    ("Visa Platinum 899092211366522299"),  # Введен длинный номер карты
    ("Счет 73654108430135874300055"),      # Введен длинный номер счета
])
def test_mask_account_card_incorrect(invalid_number: str):
    """Тестируем ввод некорректных данных карты или счета"""
    with pytest.raises(ValueError, match="Номер введен неверно"):
        mask_account_card(invalid_number)


def test_get_date():
    """Тестируем правильность преобразования даты"""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


def test_get_date_empty():
    """Тестируем отсутствие даты"""
    with pytest.raises(ValueError, match="Дата введена некорректно"):
        get_date("")


def test_get_date_incorrect():
    """Тестируем различные входные форматы даты"""
    with pytest.raises(ValueError):
        get_date("2024-14-11T02:26:18.671407")  # Неверно указан месяц

    with pytest.raises(ValueError):
        get_date("2024-03-00T02:26:18.671407")  # Неверно указана дата
