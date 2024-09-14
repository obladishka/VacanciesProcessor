from abc import ABC, abstractmethod


class FileProcessor(ABC):
    """Абстрактный класс для работы с файлами."""

    @abstractmethod
    def get_data(self, *args, **kwargs):
        """Метод получения данных из файла."""
        pass

    @abstractmethod
    def save_data(self, data: dict):
        """Метод добавления данных в файл."""
        pass

    @abstractmethod
    def delete_data(self, data: dict):
        """Метод удаления данных из файла."""
        pass
