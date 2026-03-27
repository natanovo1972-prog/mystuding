import csv
import json
from typing import Dict, List

import pandas as pd


def transactions_csv(file_path_csv: str) -> List[Dict]:
    """"Функция принимает в качестве аргумента путь к csv-файлу
       и возвращает список словарей с транзакциями"""
    try:
        with open(file_path_csv, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            return list(reader)
    except FileNotFoundError:
        print(f"Файл по пути {file_path_csv} не найден")
        return []


def transactions_excel(file_path_excel) -> List[Dict]:
    """Функция принмает в качестве аргумента путь к excel-файлу
       и возвращает список словарей с транзакциями"""
    try:
        reader_excel = pd.read_excel(file_path_excel)
        return reader_excel.to_dict(orient="records")
    except FileNotFoundError:
        print(f"Файл по пути {file_path_excel} не найден")
        return []


if __name__ == "__main__":  # pragma: no cover
    # Указываем путь к файлу csv
    file_path_csv = r'/Users/natalianovozilova/Desktop/Phyton/MyProject/data/transactions.csv'
    results_csv = transactions_csv(file_path_csv)
    list_transactions_csv = json.dumps(results_csv, indent=4, ensure_ascii=False)
    print(list_transactions_csv)

    # Указываем путь к файлу excel
    file_path_excel = r'/Users/natalianovozilova/Desktop/Phyton/MyProject/data/transactions_excel.xlsx'
    results_excel = transactions_excel(file_path_excel)
    list_transactions_excel = json.dumps(results_excel, indent=4, ensure_ascii=False)
    print(list_transactions_excel)
