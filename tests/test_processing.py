import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state(sample_dates: list) -> None:
    """Тестируем фильтрацию списка словарей по заданному статусу state"""
    assert filter_by_state(sample_dates) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}]


def test_filter_by_state_not_status() -> None:
    """Проверка работы функции при отсутствии словарей с указанным статусом state в списке"""
    input_data = [{"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                  {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}]
    expected_output: list[dict] = []
    assert filter_by_state(input_data, "EXECUTED") == expected_output


@pytest.mark.parametrize("filter_state, expected", [
    # Ожидаем список со словарем по значению "EXECUTED"
    ([{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}],
     [{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}]),
    ([{"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}],
     [{"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}]),
    # Ожидаем пустой список для значения "CANCELED"
    ([{"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}], []),
    ([{"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"}], [])])
def test_filter_by_state_any_status(filter_state: list, expected: list) -> None:
    assert filter_by_state(filter_state) == expected


def test_sort_by_date(sample_dates: list) -> None:
    assert sort_by_date(sample_dates) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}]


def test_sort_by_date_order(sample_dates: list, dates_desc: list, dates_asc: list) -> None:
    # Тестирование сортировки по датам в порядке убывания и возрастания
    assert sort_by_date(sample_dates, date=True) == dates_desc
    assert sort_by_date(sample_dates, date=False) == dates_asc


def test_sort_by_date_same() -> None:
    """Проверка работы функции при одинаковых датах"""
    same_data = [{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                 {"id": 939719570, "state": "EXECUTED", "date": "2019-07-03T02:08:58.425572"},
                 {"id": 594226727, "state": "CANCELED", "date": "2019-07-03T21:27:25.241689"},
                 {"id": 615064591, "state": "CANCELED", "date": "2019-07-03T08:21:33.419441"}]
    result = sort_by_date(same_data, date=True)
    assert [d["id"] for d in result] == [594226727, 41428829, 615064591, 939719570]


@pytest.mark.parametrize("invalid_date, expected_result", [
    # Параметризация на тестирование некорректных форматов дат
    # Ключ date отсутствует в словаре
    ([{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
      {"id": 939719570, "state": "EXECUTED"}], KeyError),
    # Значение даты - число
    ([{"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
      {"id": 615064591, "state": "CANCELED", "date": 20181014}], TypeError),
    # Date - пустая строка
    ([{"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
      {"id": 615064591, "state": "CANCELED", "date": ""}], TypeError)])
def test_sort_by_date_invalid(invalid_date: list, expected_result: type[Exception]) -> None:
    with pytest.raises(expected_result):
        sort_by_date(invalid_date)
