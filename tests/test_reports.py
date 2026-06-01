import os.path
import pytest
import pandas as pd
from src.reports import spending_by_weekday


@pytest.fixture
def sampler_transaction():
    data = {
        "Дата операции": ["2026-05-25", "2026-05-25", "2026-05-27", "2026-05-18", "2026-01-26"],
        "Сумма операции": [100.0, 200.0, 300.0, 400.0, 500.0],
    }
    return pd.DataFrame(data)


def test_spending_by_weekday_successful(sampler_transaction):
    """Тестируем корректный расчет средних трат за каждый день недели за последние три месяца"""
    result = spending_by_weekday(sampler_transaction, "2026-05-28")
    assert "Понедельник" in result.index
    assert "Среда" in result.index
    assert "Четверг" not in result.index

    assert result.loc["Понедельник", "Средние траты"] == 350.0
    assert result.loc["Среда", "Средние траты"] == 300.0


def test_spending_by_weekday_empty(sampler_transaction):
    """Тест проверяет поведение функции при  отсутствии операций за последние 3 месяца"""
    result = spending_by_weekday(sampler_transaction, "2027-02-21")
    assert result.empty
    assert "Средние траты" in result.columns


def test_spending_by_weekday_sort(sampler_transaction):
    """Тестирием, что дни недели стоят по порядку"""
    result = spending_by_weekday(sampler_transaction, "2026-05-28")
    day_order = list(result.index)
    assert day_order == ["Понедельник", "Среда"]


def test_sampler_transaction_to_file(sampler_transaction, tmp_path):
    """Тест проверяет, что декоратор успешно создает файл отчета на диске"""
    # Создаем путь к временному файлу
    test_file_path = tmp_path / "custom_report.csv"
    # Временно переопределяем имя файла для декоратора и оборачиваем функцию в декоратор с путем
    from src.reports import report

    @report(filename=str(test_file_path))
    def decorated_spending_by_weekday(*args, **kwargs):
        return spending_by_weekday(*args, **kwargs)

    # Вызываем декорированную функцию
    decorated_spending_by_weekday(sampler_transaction, date="2026-05-28")
    # Проверяем, появился ли файл на диске
    assert os.path.exists(test_file_path) is True
    # Проверяем, что данные записались в файл
    saved_df = pd.read_csv(test_file_path, sep=";")
    assert "День недели" in saved_df.columns
    assert "Средние траты" in saved_df.columns
