import json
import logging
import os

import pandas as pd
import requests
import yfinance as yf
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("utils.log", encoding="utf-8"),  # Запиcь логов в файл
        logging.StreamHandler(),  # Дублирование в консоль
    ],
)
logger = logging.getLogger(__name__)


# Определяем директорию с модулем utils.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Прописываем путь к файлу operations.xlsx
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "operations.xlsx")


def card_by_date(file_path=DATA_PATH):
    """Функция читает excel-файл с транзакциями и возвращает следующие данные: номер карты,
    общую сумму расходов и кешбэк"""
    # Загружаем данные из excel-файла
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Успешно загружен файл: {file_path}")
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return pd.DataFrame()
    # Выводим общую сумму расходов по карте
    summary = df.groupby("Номер карты")["Сумма операции"].sum().reset_index()
    # Выводим 4 последние цифры номера карты
    summary["Последние 4 цифры номера карты"] = summary["Номер карты"].str.replace("*", "")
    # Выводим кешбэк: 1 руб. за каждые 100 рублей
    summary["Кэшбэк"] = (summary["Сумма операции"] // 100).astype(int)
    result = summary[["Последние 4 цифры номера карты", "Сумма операции", "Кэшбэк"]]
    return result


def transactions_top(file_path=DATA_PATH):
    """Функция читает excel-файл и выводит топ-5 транзакций по сумме платежа"""
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Файл успешно загружен: {file_path}")
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return pd.DataFrame()
    # Группируем по сумме транзакций
    top_5 = df.sort_values(by=["Сумма операции"], ascending=False).head(5)
    # Оставляем 4 цифры из номера карты и заменяем пустые строки номера карты на "Не указана"
    top_5["Последние 4 цифры номера карты"] = (
        top_5["Номер карты"].fillna("Не указана").str.replace("*", "").replace("", "Не указана")
    )
    result = top_5[["Дата платежа", "Последние 4 цифры номера карты", "Сумма операции", "Категория", "Описание"]]
    return result


def get_setting_path():
    """Функция определяет путь к файлу user_settings.json."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    return os.path.join(root_dir, "user_settings.json")


def exchange_rate():
    """Функция формирует запрос о курсе валют с помощью ключа API и записывает данные в файл json."""
    # Загрузка переменных из .env-файла
    load_dotenv()
    # Получение значения переменной из .env-файла
    api_key = os.getenv("API_KEY")
    # Список пар валют
    pairs = "USDRUB,EURRUB"
    url = f"https://currate.ru/api/?get=rates&pairs={pairs}&key={api_key}"
    try:
        response = requests.get(url)
        # Проверка на ошибки 404, 500
        response.raise_for_status()
        currency_info = response.json()
        # Проверяем, что API  возвращает корректный статус
        if currency_info.get("status") == 200:
            rate = currency_info.get("data")
            # Создаем итоговый путь к файлу
            file_path = get_setting_path()
            # Читаем данные
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {}
            else:
                data = {}
            # Объединяем данные валют и данные акций
            data.update(rate)
            # Записываем данные в файл
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info("Данные сохранены в user_settings.json")
        else:
            logger.warning(f"Ошибка API: {currency_info.get('message')}")

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")


def action_price(ticker):
    """Функция получает стоимость акций S&P500 и записывает данные в файл json."""
    try:
        # Получаем данные через yfinance
        stock = yf.Ticker(ticker)
        today_date = stock.history(period="1d")
        if today_date.empty:
            logger.warning(f"Акция {ticker} не найдена")
            return
        price = round(float(today_date["Close"].iloc[-1]), 2)
        # Определяем путь к файлу
        file_path = get_setting_path()
        # Записываем в файл
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}  # Если файл был пуст или поврежден
        else:
            data = {}
        data[ticker] = price
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Цена {ticker} ({price}) сохранена в user_settings.json")

    except Exception as e:
        logger.error(f"Ошибка при обработке {ticker}: {e}")


if __name__ == "__main__":  # pragma: no cover
    print(card_by_date())
    get_transactions = transactions_top()
    print(get_transactions.to_string(index=False))
    exchange_rate()
    action_price("AAPL")
    action_price("AMZN")
    action_price("GOOGL")
    action_price("MSFT")
    action_price("TSLA")
