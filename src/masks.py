def get_mask_card_number(number_card: str) -> str:
    """Функция принимает в качестве аргумента номер карты в виде строки и возвращает ее маску"""
    if len(number_card) < 16 or len(number_card) > 16:
        raise ValueError("Номер должен содержать 16 цифр")
    return number_card[:4] + " " + number_card[4:6] + "** ****" + " " + number_card[-4:]


print(get_mask_card_number("7000792289606361"))


def get_mask_account(count_number: str) -> str:
    """Функция принимает в качестве аргумента номер счета в виде строки и возвращает его маску"""
    if " " in count_number or "-" in count_number:
        raise ValueError ("Номер счета должен содержать 20 цифр")
    if len(count_number) < 20 or len(count_number) > 20:
        raise ValueError("Номер счета должен содержать 20 цифр")
    return "**" + count_number[-4:]


print(get_mask_account("73654108430135874305"))
