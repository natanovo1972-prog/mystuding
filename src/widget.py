from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """Функция принимает строку c типом и номером карты или счета, и возвращает строку с замаскированным номером"""
    if not isinstance (account_card, str) or not account_card.strip():
        return ""
    account_card_info = account_card.rsplit(' ', 1)
    if len(account_card_info) > 1:
        name = account_card_info[0]
        number = account_card_info[1]
    if "Счет" in name:
        return f"{name} **{number[-4:]}"
    else:
        return f"{name} {get_mask_card_number(number)}"
    return account_card


def get_date(date: str) -> str:
    """Функция принимает строку в формате 2024-03-11Т02:26:18.671407 и возвращает строку в формате ДД.ММ.ГГГГ"""
    if date == "":
        raise ValueError("Дата введена некорректно")
    try:
        dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        clean_date = date.replace('Z', '')
        dt = datetime.strptime(clean_date, "%Y-%m-%dT%H:%M:%S")

    return dt.strftime("%d.%m.%Y")


if __name__ == "__main__":  # pragma: no cover
    test_1 = "Visa Platinum 8990922113665229"
    test_2 = "Счет 73654108430135874305"
    # print(mask_account_card(test_1))
    # print(mask_account_card(test_2))

    test_date = "2024-03-11T02:26:18.671407"
    print(get_date(test_date))
