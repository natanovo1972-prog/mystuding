import logging
import os
import pandas as pd
from typing import Optional, Callable
from functools import wraps, partial
from datetime import datetime

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H-%M-%S"
)
logger = logging.getLogger(__name__)


def report(func: Optional[Callable] = None, *, filename: Optional[str] = None):
    """Декоратор для сохранения результатов функции в CSV-файл"""
    if func is None:
        return partial(report, filename=filename)

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Начало формирования отчета: {func.__name__}")
        # Вызываем функцию отчета
        result = func(*args, **kwargs)
        # Проверяем, что функция вернула DataFrame
        if isinstance(result, pd.DataFrame):
            # Определяем имя файла
            if filename:
                final_file = filename
            else:
                # Имя файла по умолчанию
                timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                final_file = f"report_{timestamp}.csv"
            try:
                # Сохраняем в файл CSV
                result.to_csv(final_file, encoding="utf-8-sig", sep=";")
                logger.info(f"Отчет успешно сформирован и сохранен в файл: {os.path.abspath(final_file)}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении отчета в файл {final_file}: {e}")
        else:
            logger.warning(f"Функция {func.__name__} не DataFrame. Файл не сохранен")
        return result

    return wrapper


@report
def spending_by_weekday(transaction: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Функция принимает в качестве аргумента DataFrame и опциональную дату
    и возвращает средние траты в каждый день недели за последние три месяца
    от переданной даты"""
    df = transaction.copy().reset_index(drop=True)
    df["Дата операции"] = df["Дата операции"].astype(str).str.replace(".", "-", regex=False)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True, errors="coerce")
    # Определяем начальную и конечную дату
    if date:
        end_date = pd.to_datetime(date).replace(hour=23, minute=59, second=59)
    else:
        end_date = pd.Timestamp.now()
    start_date = end_date.replace(hour=0, minute=0, second=0) - pd.DateOffset(months=3)
    # Создаем маску для нужного диапазона дат
    mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)
    # Фильтруем данные в соответствии с маской
    filtered_df = df.loc[mask].copy().reset_index(drop=True)
    if filtered_df.empty:
        return pd.DataFrame(columns=["Средние траты"])

    daily_spend = (
        filtered_df.groupby("Дата операции")["Сумма операции"]
        .sum()
        .reset_index()
    )
    # Определяем номера дней недели
    daily_spend["number_weekday"] = daily_spend["Дата операции"].dt.weekday
    mean_spend = daily_spend.groupby("number_weekday")["Сумма операции"].mean()
    week_days = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье",
    }

    result_data = []
    for day_num in sorted(mean_spend.index):
        result_data.append(
            {
                "День недели": week_days[day_num],
                "Средние траты": round(mean_spend[day_num], 2),
            }
        )
    if result_data:
        result = pd.DataFrame(result_data).set_index("День недели")
    else:
        result = pd.DataFrame(columns=["Средние траты"])

    return result


# Определяем директорию с модулем reports.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Прописываем путь к файлу operations.xlsx
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "operations.xlsx")

my_data = pd.read_excel(DATA_PATH)


if __name__ == "__main__":  # pragma: no cover
    final_report = spending_by_weekday(my_data, date="2018-10-28")
    print(final_report)
