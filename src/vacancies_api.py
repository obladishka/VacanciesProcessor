from abc import ABC, abstractmethod


class VacanciesApi(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями."""

    @abstractmethod
    def _get_response(self, params: dict):
        """Метод для подключения к API."""
        pass

    @abstractmethod
    def get_vacancies(self, text: str, per_page: int):
        """Метод для получения вакансий."""
        pass
