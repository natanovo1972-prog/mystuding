from masks import get_mask_card_number
from masks import get_mask_account
from datetime import datetime

def mask_account_card(account_card: str) -> str:
    """Функция принимает в качестве аргумента строку, содержащую тип и номер карты или счета, и возвращает строку с замаскированным номером"""
    account_card_info = account_card.rsplit(' ', 1)
    if "Счет" in account_card:
        return f"{account_card_info[0]} {get_mask_account(account_card_info[1])}"
    else:
        return f"{account_card_info[0]} {get_mask_card_number(account_card_info[1])}"


def get_date(date: str) -> str:
    """Функция принимает на вход строку в формате 2024-03-11Т02:26:18.671407 и возвращает строку в формате ДД.ММ.ГГГГ"""
    current_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    return current_date.strftime("%d.%m.%Y")


if __name__ == "__main__":
    test_1 = "Visa Platinum 8990922113665229"
    test_2 = "Счет 73654108430135874305"
    print(mask_account_card(test_1))
    print(mask_account_card(test_2))

    test_date = "2024-03-11T02:26:18.671407"
    print(get_date(test_date))





