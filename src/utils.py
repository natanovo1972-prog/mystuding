import json
import os


def fin_transaction(filepath: str) -> list[dict]:
    """Функция приинмает путь до JSON-файла и возвращает список словарей
       с данными о финансовых транзакциях"""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            fin_trans = json.load(file)
    except json.JSONDecodeError:  # В файле ошибка
        return []
    except FileNotFoundError:  # Файл не найден
        return []
    if not isinstance(fin_trans, list):  # Файл не является списком
        return []

    return fin_trans


if __name__ == "__main__":  # pragma: no cover
    skript_folder = os.path.dirname(__file__)  # Определяем путь к текущей директории проекта
    file_path = os.path.join(skript_folder, "..", "data", "operations.json")  # Определяем полный путь к файлу
    result = fin_transaction(file_path)
    print(result)
