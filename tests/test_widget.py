import pytest

from src.widget import mask_account_card


def test_mask_account_card():
    """Тест для проверки функции маскировки в зависимости от типа входных данных (карта или счет)"""
    assert mask_account_card("Visa Platinum 8990922113665229") == "Visa Platinum 8990 92** **** 5229"
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"


@pytest.mark.parametrize("value, expected", [("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
("Счет 73654108430135874305", "Счет **4305"), ("MasterCard 4567832197623451", "MasterCard 4567 83** **** 3451")])

def test_mask_account_card(value, expected):
    assert mask_account_card("value") == "expected"


def test_mask_account_card_incorrect():
    """Тестирование функции на обработку некорректных входных данных"""
    with pytest.raises(ValueError, match="Номер неправильной длины") as exc_info:
        mask_account_card("Visa Platinum 8990922113665") #Тестируем короткий номер

    with pytest.raises(ValueError, match="Номер неправильной длины") as exc_info:
        mask_account_card("Счет 7365410843013587430005") #Тестируем длинный номер

    with pytest.raises(ValueError, match="Номер неправильной длины") as exc_info:
        mask_account_card("") #Тестируем пустую строку