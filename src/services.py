import json
import logging
import os

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("services.log", encoding="utf-8"),  # Запиcь логов в файл
        logging.StreamHandler(),  # Дублирование в консоль
    ],
)
logger = logging.getLogger(__name__)


# Определяем директорию с модулем services.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Прописываем путь к файлу operations.xlsx
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "operations.xlsx")


def transactions_by_phone(file_path=DATA_PATH):
    """Функция принимает путь к файлу с транзакциями и возвращает JSON со всеми транзакиями,
    содержащими телефонные номера"""
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Успешно загружен файл: {file_path}")
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return json.dumps([])
    number_phone = r"(?:\+7|8)?\s?\(?\d{3}\)?\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}"
    df_stroke = df["Описание"].fillna("").str.contains(number_phone, regex=True)
    filtered_df = df[df_stroke]
    dict_list = filtered_df.to_dict(orient="records")
    result = json.dumps(dict_list, indent=4, ensure_ascii=False)
    return result


if __name__ == "__main__":  # pragma: no cover
    print(transactions_by_phone())
