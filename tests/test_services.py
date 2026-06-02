import json
from unittest.mock import patch

import pandas as pd
import pytest

from src.services import transactions_by_phone


@pytest.fixture
def data_for_test():
    return pd.DataFrame({"Описание": ["MTC +7 906 123-45-67", "Перевод", "Билайн +7 906 891-11-12"]})


def test_transaction_by_phone_successful(data_for_test):
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = data_for_test
        # Вызов функции
        json_result = transactions_by_phone("test.xlsx")
        # Превращаем json-строку в список Python для проверки
        result_list = json.loads(json_result)
        # Проверки
        assert len(result_list) == 2
        assert result_list[0]["Описание"] == "MTC +7 906 123-45-67"
        assert result_list[1]["Описание"] == "Билайн +7 906 891-11-12"


def test_transaction_by_phone_file_not_found():
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        json_result = transactions_by_phone("file_not_exist.xlsx")
        assert json_result == "[]"
