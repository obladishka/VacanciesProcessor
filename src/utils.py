import re

import requests

from src.vacancy import Vacancy


def get_currencies_rates() -> dict:
    """Функция для получения актуального курса валют."""
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    response = requests.get(url)
    status_code = response.status_code

    if status_code == 200:
        return response.json()["Valute"]


def convert_to_ruble(currencies_rates: dict, currency: str) -> float:
    """Функция для преобразования суммы в рубли."""
    value = currencies_rates.get(currency, {}).get("Value")
    nominal = currencies_rates.get(currency, {}).get("Nominal")
    return round(value / nominal, 2)


def dict_to_vacancy(vacancies: list[dict]) -> list[Vacancy]:
    """Функция для преобразования списка словарей в список объектов класса Vacancy."""
    return [Vacancy.new_vacancy(vacancy) for vacancy in vacancies]


def filter_by_word(vacancies: list[dict], params: list[str]) -> list[dict]:
    """Функция для фильтрации вакансий с определёнными словами в названии или требованиях."""
    vacancies = dict_to_vacancy(vacancies)
    patterns = [rf"{re.escape(re.sub(r"ть|сти|вать", "", search_str))}?.*" for search_str in params]
    return [
        vacancy.to_dict()
        for vacancy in vacancies
        if any(
            re.search(pattern, vacancy.name, flags=re.IGNORECASE)
            or re.search(pattern, vacancy.responsibilities, flags=re.IGNORECASE)
            for pattern in patterns
        )
    ]


def filter_by_place(vacancies: list[dict], place: str) -> list[dict]:
    """Функция для фильтрации вакансий по месту работы."""
    vacancies = dict_to_vacancy(vacancies)
    return [vacancy.to_dict() for vacancy in vacancies if vacancy.place.lower() == place.lower()]


def sort_by_salary(vacancies: list[dict], top_n: int) -> list[dict]:
    """Функция для сортировки вакансий по зарплате."""
    if top_n <= 0 or top_n > len(vacancies):
        raise ValueError(f"Введите число в диапазоне от 0 до {len(vacancies)}.")

    rates = get_currencies_rates()
    vacancies = dict_to_vacancy(vacancies)
    sorted_vacancies = sorted(
        vacancies,
        key=lambda x: x.max_salary if x.currency == "RUR" else x.max_salary * convert_to_ruble(rates, x.currency),
        reverse=True,
    )
    return [vacancy.to_dict() for vacancy in sorted_vacancies[:top_n]]
