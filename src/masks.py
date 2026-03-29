import logging
import os

Base_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем путь к папке src, где лежит модуль masks
Log_dir = os.path.join(Base_dir, "..", "logs")  # Поднимаемся на уровень выше в корне проекта и находим там папку logs
log_file_path = os.path.join(Log_dir, "masks.log")  # Соединяем путь к папке с именем файла

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s) - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(number_card: str) -> str:
    """Функция принимает в качестве аргумента номер карты в виде строки и возвращает ее маску"""
    if len(number_card) < 16 or len(number_card) > 16:
        logger.error(f"Ошибка номера карты: {number_card}")
        raise ValueError("Номер введен неверно")
    logger.debug(f"Создана маска карты: {number_card}")
    return number_card[:4] + " " + number_card[4:6] + "** ****" + " " + number_card[-4:]


print(get_mask_card_number("7000792289606361"))


def get_mask_account(count_number: str) -> str:
    """Функция принимает в качестве аргумента номер счета в виде строки и возвращает его маску"""
    if " " in count_number or "-" in count_number:
        logger.error(f"Ошибка номера счета: {count_number}")
        raise ValueError("Номер введен неверно")
    if len(count_number) < 20 or len(count_number) > 20:
        logger.error(f"Ошибка длины номера счета: {count_number}")
        raise ValueError("Номер введен неверно")
    logger.debug(f"Создана маска счета: {count_number}")
    return "**" + count_number[-4:]


print(get_mask_account("73654108430135874305"))
