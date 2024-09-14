import pytest

from src.vacancy import Vacancy


def test_vacancy_init(vacancy_1, vacancy_2):
    """Тестирует инициализацию объектов класса."""
    assert vacancy_1.vac_id == "106735215"
    assert vacancy_1.name == "Диспетчер чатов (в Яндекс)"
    assert vacancy_1.max_salary == 44000
    assert vacancy_1.currency == "RUR"

    assert vacancy_2.place == "Алматы"
    assert vacancy_2.responsibilities == (
        "Работать с торговыми точками канала BC и HoReCa. "
        "Работать в «полевых» условиях. "
        "Посещать торговые точки на вверенной территории. "
    )
    assert vacancy_2.url == "https://hh.ru/vacancy/106500391"


def test_new_vacancy(vacancy_dict):
    """Тестирует создание объекта класса из словаря."""
    vacancy = Vacancy.new_vacancy(vacancy_dict)
    assert vacancy.vac_id == "107217584"
    assert vacancy.max_salary == 800
    assert vacancy.url == "https://hh.ru/vacancy/107217584"


def test_vacancy_salary_error(vacancy_dict):
    """Тестирует верификацию зарплаты (отрицательная зп) при создании объекта класса."""
    vacancy_dict["max_salary"] = -800
    with pytest.raises(ValueError, match="Зарплата не может быть отрицательной."):
        Vacancy.new_vacancy(vacancy_dict)


def test_vacancy_empty_salary(vacancy_dict):
    """Тестирует верификацию зарплаты (отсутствие зп) при создании объекта класса."""
    vacancy_dict["max_salary"] = None
    assert Vacancy.new_vacancy(vacancy_dict).max_salary == 0


def test_vacancy_wrong_url(vacancy_dict):
    """Тестирует верификацию ссылки при создании объекта класса."""
    vacancy_dict["url"] = "https://wrong_url.com"
    assert Vacancy.new_vacancy(vacancy_dict).url is None


def test_vacancies_salary_comparison(vacancy_1, vacancy_2):
    """Тестирует сравнение объектов класса по зп."""
    assert vacancy_1 <= vacancy_2


def test_vacancy_salary_comparison_to_num(vacancy_1, vacancy_dict):
    """Тестирует сравнение зп объекта класса с числом."""
    assert vacancy_1 >= 30000
    assert vacancy_1 >= vacancy_dict.get("max_salary")


def test_vacancy_salary_comparison_wrong_object(vacancy_1, vacancy_dict):
    """Тестирует возникновение ошибки при неверном сравнении данных."""
    with pytest.raises(
        ValueError, match="Сравнение возможно только между объектами класса или между объектами класса и числами."
    ):
        print(vacancy_1 >= vacancy_dict)
