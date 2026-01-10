from src.widget import mask_account_card, get_date
import pytest


def test_mask_account_card():
    """Тестируем, что функция корректно распознает и применяет
    нужный тип маскировки в зависимости от типа входных данных"""
    assert mask_account_card("Visa Platinum 8990922113665229") == "Visa Platinum 8990 92** **** 5229"
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"


@pytest.mark.parametrize("account, expected", [("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
                                               ("Счет 73654108430135874305", "Счет **4305")])
def test_mask_account_card(account, expected):
    assert mask_account_card(account) == expected


def test_mask_account_card_incorrect():
    """Тестируем ввод некорректных данных карты или счета"""
    with pytest.raises(ValueError, match="Номер введен неверно") as ex_info:
        mask_account_card("Visa Platinum 89909221136652") #Тестируем короткий номер
        mask_account_card("Счет 736541084301358743")

    with pytest.raises(ValueError, match="Номер введен неверно") as ex_info:
        mask_account_card("Visa Platinum 899092211366522299") #Тестируем длинный номер
        mask_account_card("Счет 73654108430135874300055")


def test_get_date():
    """Тестируем правильность преобразования даты"""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


def test_get_date_empty():
    """Тестируем отсутствие даты"""
    with pytest.raises(ValueError, match="Дата введена некорректно") as ex_info:
        get_date("")

def test_get_date_incorrect():
    """Тестируем различные входные форматы даты"""
    with pytest.raises(ValueError):
        get_date("2024-14-11T02:26:18.671407") #Неверно указан месяц

    with pytest.raises(ValueError):
        get_date("2024-03-00T02:26:18.671407") #Неверно указана дата