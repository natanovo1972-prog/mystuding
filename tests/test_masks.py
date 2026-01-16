import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize("input_number, expected_mask", [
    ("7000792289606361", "7000 79** **** 6361"),
    ("1111222233334444", "1111 22** **** 4444")])
def test_mask_card_number(input_number: str, expected_mask: str) -> None:
    """Тестирование правильности маскирования номера карты со стандартным 16-м номером"""
    assert get_mask_card_number(input_number) == expected_mask


@pytest.mark.parametrize("invalid_number", [
    ("700079228960636"),  # Введенный номер меньше 16 символов
    ("70007922896063611"),  # Введенный номер больше 16 символов
    (""),                    # Пустая строка
    ("111")                  # Короткий номер
])
def test_mask_card_number_incorrect(invalid_number: str) -> None:
    """Проверка работы функции на различных форматах номеров карт, включая граничные случаи
    и нестандартрные длины номеров карт"""
    with pytest.raises(ValueError, match="Номер введен неверно"):
        get_mask_card_number(invalid_number)


def test_mask_account() -> None:
    """Проверка правильности маскирования номера счета"""
    assert get_mask_account("73654108430135874305") == "**4305"


@pytest.mark.parametrize("invalid_account", [
    ("7365 4108 4301 3587 4305"),  # Номер счета введен с пробелами
    ("736541084301358743005"),     # Номер счета больше 20 цифр
    ("7365410843013587")           # Номер счета меньше 20 цифр
])
def test_mask_account_different_format(invalid_account: str) -> None:
    """Проверка работы функции с различными форматами и длинами номера счета"""
    with pytest.raises(ValueError, match="Номер введен неверно"):
        get_mask_account(invalid_account)
