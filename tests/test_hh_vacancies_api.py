from unittest import mock
from unittest.mock import patch

import pytest
import requests


def test_hh(hh):
    """Тестирует инициализацию объектов класса."""
    assert len(hh.__dict__) == 4
    assert [type(value) for value in hh.__dict__.values()] == [str, dict, dict, list]


@patch("src.hh_vacancies_api.requests.get")
def test_hh_get_vacancies(mock_get, hh, api_response):
    """Тестирует нормальную работу метода."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = api_response

    assert hh.get_vacancies("Python")[0]["name"] == "Junior Python разработчик"
    mock_get.assert_called_with(
        "https://api.hh.ru/vacancies",
        headers={"User-Agent": "HH-User-Agent"},
        params={"text": "Python", "page": 20, "per_page": 100},
    )

    assert hh.get_vacancies("Python", 20)[0]["name"] == "Junior Python разработчик"
    mock_get.assert_called_with(
        "https://api.hh.ru/vacancies",
        headers={"User-Agent": "HH-User-Agent"},
        params={"text": "Python", "page": 100, "per_page": 20},
    )


def test_hh_get_vacancies_request_error(hh, capsys):
    """Тестирует работу метода при возникновении ошибки запроса."""
    with mock.patch("requests.get", side_effect=requests.exceptions.RequestException("Something went wrong")):
        hh.get_vacancies("Python", 20)
    assert capsys.readouterr().out.strip() == "Something went wrong"


def test_hh_get_vacancies_wrong_params(hh):
    """Тестирует работу метода при передаче неверных параметров."""
    with pytest.raises(ValueError, match="Количество элементов должно быть от 1 до 100."):
        hh.get_vacancies("Python", 120)

    with pytest.raises(ValueError, match="Количество элементов должно быть от 1 до 100."):
        hh.get_vacancies("Python", 0)
