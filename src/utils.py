import json
import logging
import os

Base_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем путь к папке src, где лежит модуль utils
Log_dir = os.path.join(Base_dir, "..", "logs")  # Поднимаемся на уровень выше в корне проекта и находим там папку logs
log_file_path = os.path.join(Log_dir, "utils.log")  # Соединяем путь к папке с именем файла

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s) - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def fin_transaction(filepath: str) -> list[dict]:
    """Функция приинмает путь до JSON-файла и возвращает список словарей
       с данными о финансовых транзакциях"""
    try:
        logger.debug(f"Загружаем данные из {filepath}")
        with open(filepath, "r", encoding="utf-8") as file:
            fin_trans = json.load(file)
    except json.JSONDecodeError as e:  # В файле ошибка
        logger.error(f"Ошибка в формате JSON: {e}")
        return []
    except FileNotFoundError:  # Файл не найден
        logger.error(f"Файл не найден по пути: {filepath}")
        return []
    if not isinstance(fin_trans, list):  # Файл не является списком
        logger.error(f"Данные файла не являются списком")
        return []

    return fin_trans


if __name__ == "__main__":  # pragma: no cover
    skript_folder = os.path.dirname(__file__)  # Определяем путь к текущей директории проекта
    file_path = os.path.join(skript_folder, "..", "data", "operations.json")  # Определяем полный путь к файлу
    result = fin_transaction(file_path)
    print(result)
