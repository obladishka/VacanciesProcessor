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
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 0}
        self.__vacancies = []

    def _get_response(self, params: dict) -> None | dict:
        """Метод для подключения к API сайта hh.ru."""

        try:
            self.response = requests.get(self.__url, headers=self.__headers, params=params)
        except requests.exceptions.RequestException as ex:
            print(ex)
        else:
            if self.response.status_code == 200:
                return self.response.json()

    def get_vacancies(self, text: str, per_page: int = 100) -> list:
        """Метод для получения вакансий."""

        if per_page > 100 or per_page <= 0:
            raise ValueError("Количество элементов должно быть от 1 до 100.")

        self.__params["text"] = text
        self.__params["per_page"] = per_page

        while self.__params.get("page") < 2000 // per_page:
            if not self._get_response(self.__params):
                break
            if self._get_response(self.__params):
                vacancies = self._get_response(self.__params).get("items")
                self.__vacancies.extend(vacancies)
            self.__params["page"] += 1

        return self.__vacancies
