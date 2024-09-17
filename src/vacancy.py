import re


class Vacancy:
    """Класс для работы с вакансиями."""

    __slots__ = ("vac_id", "name", "max_salary", "currency", "place", "responsibilities", "url")

    vac_id: str
    name: str
    max_salary: float
    currency: str
    place: str
    responsibilities: str
    url: str

    def __init__(self, vac_id, name, max_salary, currency, place, responsibilities, url):
        """Метод для инициализации объектов класса."""
        self.vac_id = vac_id
        self.name = name
        self.max_salary = self.__is_valid_salary(max_salary)
        self.currency = currency
        self.place = place
        self.responsibilities = responsibilities if responsibilities else ""
        self.url = self.__is_valid_ulr(url)

    def __le__(self, other):
        """Метод сравнения зарплат меньше или равно."""
        max_salary = self.__verify_data(other)
        return self.max_salary <= max_salary

    def __ge__(self, other):
        """Метод сравнения зарплат больше или равно."""
        max_salary = self.__verify_data(other)
        return self.max_salary >= max_salary

    def to_dict(self):
        """Метод преобразования вакансии в словарь."""
        return {
            "vac_id": self.vac_id,
            "name": self.name,
            "max_salary": self.max_salary,
            "currency": self.currency,
            "place": self.place,
            "responsibilities": self.responsibilities,
            "url": self.url,
        }

    @classmethod
    def new_vacancy(cls, vacancy: dict):
        """Метод для создания новых вакансий из словаря."""
        if type(vacancy) is dict and all(i in vacancy.keys() for i in cls.__slots__):
            return cls(**vacancy)

    @classmethod
    def __verify_data(cls, other):
        """Метод верификации объекта для сравнения."""
        if not isinstance(other, (int, cls)):
            raise ValueError("Сравнение возможно только между объектами класса или между объектами класса и числами.")
        return other if isinstance(other, int) else other.max_salary

    @staticmethod
    def __is_valid_salary(salary: float):
        """Метод для валидации зарплаты."""
        if not salary:
            return 0
        if salary < 0:
            raise ValueError("Зарплата не может быть отрицательной.")
        return salary

    @staticmethod
    def __is_valid_ulr(url: str):
        """Метод для валидации ссылки на вакансию."""
        pattern = re.compile(
            r"^(?:http|ftp)s?://"
            r"(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?$)"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        if re.match(pattern, url) is not None:
            return url
