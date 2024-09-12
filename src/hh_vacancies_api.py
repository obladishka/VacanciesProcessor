import requests

from src.vacancies_api import VacanciesApi


class HHVacanciesApi(VacanciesApi):
    """Класс для работы с платформой hh.ru"""

    url: str
    headers: dict
    params: dict
    vacancies: list

    def __init__(self):
        """Метод для инициализации объектов класса."""
        self.__url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "page": 0, "per_page": 0}
        self.vacancies = []

    def _get_response(self, params: dict) -> None | dict:
        """Метод для подключения к API сайта hh.ru."""

        try:
            self.response = requests.get(self.__url, headers=self.headers, params=params)
        except requests.exceptions.RequestException as ex:
            print(ex)
        else:
            if self.response.status_code == 200:
                return self.response.json()

    def get_vacancies(self, text: str, per_page: int = 100) -> list:
        """Метод для получения вакансий."""

        if per_page > 100 or per_page <= 0:
            raise ValueError("Количество элементов должно быть от 1 до 100.")

        self.params["text"] = text
        self.params["per_page"] = per_page

        while self.params.get("page") < 2000 // per_page:
            if not self._get_response(self.params):
                break
            if self._get_response(self.params):
                vacancies = self._get_response(self.params).get("items")
                self.vacancies.extend(vacancies)
            self.params["page"] += 1

        return self.vacancies
