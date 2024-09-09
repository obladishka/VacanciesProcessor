from abc import ABC, abstractmethod


class Parser(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями."""

    @abstractmethod
    def __get_response(self):
        """Метод для подключения к API."""
        pass

    @abstractmethod
    def get_vacancies(self):
        """Метод для получения вакансий."""
        pass
