import json
import os

from src.file_processor import FileProcessor
from src.vacancy import Vacancy


class JSONProcessor(FileProcessor):
    """Класс для работы с JSON-файлами."""

    file_name: str
    file_path: str
    vacancies: list
    vacancies_ids: list

    __BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

    def __init__(self, vacancies: list, file_name=None):
        """Метод для инициализации объектов класса."""
        self.__file_name = self.__validate_file_name(file_name) if file_name else "vacancies.json"
        self.__file_path = os.path.join(self.__BASE_PATH, self.__file_name)
        self.__vacancies, self.__vacancies_ids = self.get_data()
        self.__vacancies.extend(self.__validate_vacancies(vacancies))

        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(self.__vacancies, f, ensure_ascii=False, indent=4)

    def get_data(self):
        """Метод получения данных из файла."""
        try:
            with open(self.__file_path, encoding="utf-8") as f:
                self.__vacancies = json.load(f)
                self.__vacancies_ids = [vacancy.get("vac_id") for vacancy in self.__vacancies]
        except FileNotFoundError:
            return [], []
        except json.JSONDecodeError or json.encoder.JSONEncoder:
            return [], []
        else:
            return self.__vacancies, self.__vacancies_ids

    def add_data(self, data: dict):
        """Метод добавления данных в файл."""
        self.get_data()
        if self.__validate_data(data) and data.get("vac_id") not in self.__vacancies_ids:
            self.__vacancies.append(data)
            self.__vacancies_ids.append(data.get("vac_id"))

            with open(self.__file_path, "w", encoding="utf-8") as f:
                json.dump(self.__vacancies, f, ensure_ascii=False, indent=4)

    def delete_data(self, data: dict):
        """Метод удаления данных из файла."""
        self.get_data()
        if self.__validate_data(data):
            if data.get("vac_id") not in self.__vacancies_ids:
                raise ValueError(
                    f"Вакансия с номером {data.get("vac_id")} отсутствует в файле и не может быть удалена."
                )

            for i, vacancy in enumerate(self.__vacancies):
                if vacancy.get("vac_id") == data.get("vac_id"):
                    self.__vacancies.pop(i)
                    self.__vacancies_ids.pop(i)
                    break

            with open(self.__file_path, "w", encoding="utf-8") as f:
                json.dump(self.__vacancies, f, ensure_ascii=False, indent=4)

    def __validate_vacancies(self, vacancies: list):
        """Метод для валидации данных, записываемых в файл при инициализации объекта."""
        if type(vacancies) is not list or any(type(vacancy) is not dict for vacancy in vacancies):
            raise ValueError("Данные должны передаваться в виде списка словарей.")
        return [
            vacancy
            for vacancy in vacancies
            if self.__validate_data(vacancy) and vacancy.get("vac_id") not in self.__vacancies_ids
        ]

    @staticmethod
    def __validate_data(data: dict):
        """Метод для валидации добавляемых или удаляемых данных."""
        if type(data) is not dict:
            raise ValueError(f"Данные {data} должны передаваться в виде словаря.")
        if not Vacancy.new_vacancy(data):
            raise ValueError(f"Данные {data} должны соответствовать атрибутам класса Vacancy.")
        return data

    @staticmethod
    def __validate_file_name(file_name: str):
        """Метод для валидации имени файла."""
        if file_name.lower().split(".")[-1] != "json":
            raise ValueError("Класс предназначен для работы с JSON-файлами.")
        return file_name
