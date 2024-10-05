from unittest.mock import patch

import pytest

from src.utils import (convert_to_ruble, dict_to_vacancy, filter_by_place, filter_by_word, get_currencies_rates,
                       sort_by_salary)
from src.vacancy import Vacancy


@patch("src.utils.requests.get")
def test_get_currencies_rates(mock_get, api_response_currencies, currencies_rates):
    """Тестирует получение текущего курса валют."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = api_response_currencies
    assert get_currencies_rates() == currencies_rates


@patch("src.utils.requests.get")
def test_get_currencies_rates_denied_request(mock_get):
    """Тестирует работу функции, когда запрос был заблокирован."""
    mock_get.return_value.status_code = 403
    mock_get.return_value.reason = "Forbidden"
    assert get_currencies_rates() is None


@pytest.mark.parametrize(
    "currency, result",
    [
        ("USD", 87.99),
        ("KZT", 0.18),
    ],
)
def test_convert_to_ruble(currencies_rates, currency, result):
    """Тестирует преобразования суммы в рубли."""
    assert convert_to_ruble(currencies_rates, currency) == result


def test_convert_to_ruble_currency_not_found(currencies_rates):
    """Тестирует преобразования суммы в рубли при отсутствии данных по курсу валюты."""
    assert convert_to_ruble(currencies_rates, "UZS") == 0


def test_dict_to_vacancy(vacancies_list):
    """Тестирует преобразование списка словарей в список вакансий."""
    vacancies = dict_to_vacancy(vacancies_list)
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[1].name == "Торговый представитель"


def test_filter_by_word(vacancies_list):
    """Тестирует фильтрацию вакансий по ключевым словам."""
    assert filter_by_word(vacancies_list, ["клиенты", "партнеры"]) == [vacancies_list[0]]
    assert filter_by_word(vacancies_list, ["торговый"]) == [vacancies_list[1]]
    assert filter_by_word(vacancies_list, ["работать"]) == vacancies_list
    assert filter_by_word(vacancies_list, ["python"]) == []


def test_filter_by_place(vacancies_list):
    """Тестирует фильтрацию вакансий по месту."""
    assert filter_by_place(vacancies_list, "россия") == [vacancies_list[0]]
    assert filter_by_place(vacancies_list, "Алматы") == [vacancies_list[1]]
    assert filter_by_place(vacancies_list, "москва") == []


def test_sort_by_salary(vacancies_list):
    """Тестирует вывод топа вакансий по зп."""
    assert sort_by_salary(vacancies_list, 2) == vacancies_list[::-1]


@pytest.mark.parametrize("top_n", [0, -1, 3])
def test_sort_by_salary_wrong_n(vacancies_list, top_n):
    """Тестирует работу функции при неверной передаче n."""
    with pytest.raises(ValueError, match="Введите число в диапазоне от 1 до 2."):
        sort_by_salary(vacancies_list, top_n)
