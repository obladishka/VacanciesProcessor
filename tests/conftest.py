import pytest

from src.hh_vacancies_api import HHVacanciesApi
from src.vacancy import Vacancy


@pytest.fixture
def hh():
    return HHVacanciesApi()


@pytest.fixture
def api_response():
    response = {
        "items": [
            {
                "id": "106571399",
                "premium": False,
                "name": "Junior Python разработчик",
                "department": None,
                "has_test": False,
                "response_letter_required": True,
                "area": {"id": "1", "name": "Москва", "url": "https://api.hh.ru/areas/1"},
                "salary": {"from": 125000, "to": None, "currency": "RUR", "gross": False},
                "type": {"id": "open", "name": "Открытая"},
                "address": None,
                "response_url": None,
                "sort_point_distance": None,
                "published_at": "2024-08-30T15:21:28+0300",
                "created_at": "2024-08-30T15:21:28+0300",
                "archived": False,
                "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=106571399",
                "insider_interview": None,
                "url": "https://api.hh.ru/vacancies/106571399?host=hh.ru",
                "alternate_url": "https://hh.ru/vacancy/106571399",
                "relations": [],
                "employer": {
                    "id": "11075572",
                    "name": "Monogramm",
                    "url": "https://api.hh.ru/employers/11075572",
                    "alternate_url": "https://hh.ru/employer/11075572",
                    "logo_urls": None,
                    "vacancies_url": "https://api.hh.ru/vacancies?employer_id=11075572",
                    "accredited_it_employer": False,
                    "trusted": True,
                },
                "snippet": {
                    "requirement": "Базовые знания Python. Понимание ООП. "
                    "Опыт работы с фреймворками (например, Django, Flask). Знание SQL. "
                    "Базовые знания HTML, CSS, JavaScript. ",
                    "responsibility": "Разработка и поддержка backend части приложения на Python. "
                    "Работа с базами данных (например, PostgreSQL, MongoDB). "
                    "Написание чистого, эффективного и хорошо...",
                },
                "contacts": None,
                "schedule": {"id": "flexible", "name": "Гибкий график"},
                "working_days": [],
                "working_time_intervals": [],
                "working_time_modes": [],
                "accept_temporary": False,
                "professional_roles": [{"id": "96", "name": "Программист, разработчик"}],
                "accept_incomplete_resumes": False,
                "experience": {"id": "noExperience", "name": "Нет опыта"},
                "employment": {"id": "full", "name": "Полная занятость"},
                "adv_response_url": None,
                "is_adv_vacancy": False,
                "adv_context": None,
            },
        ],
        "found": 13558,
        "pages": 20,
        "page": 0,
        "per_page": 100,
        "clusters": None,
        "arguments": None,
        "fixes": None,
        "suggests": None,
        "alternate_url": "https://hh.ru/search/vacancy?enable_snippets=true",
    }
    return response


@pytest.fixture
def vacancy_1():
    return Vacancy(
        "106735215",
        "Диспетчер чатов (в Яндекс)",
        44000,
        "RUR",
        "Россия",
        "Работать с клиентами или партнерами для решения разнообразных ситуаций. "
        "Развивать процессы и инструменты для улучшения качества сервисов.",
        "https://hh.ru/vacancy/106735215",
    )


@pytest.fixture
def vacancy_2():
    return Vacancy(
        "106500391",
        "Торговый представитель",
        350000,
        "KZT",
        "Алматы",
        "Работать с торговыми точками канала BC и HoReCa. Работать в «полевых» условиях. "
        "Посещать торговые точки на вверенной территории. ",
        "https://hh.ru/vacancy/106500391",
    )


@pytest.fixture
def vacancy_dict():
    return {
        "vac_id": "107217584",
        "name": "Специалист пункта выдачи заказов WILDBERRIES",
        "max_salary": 800,
        "currency": "BYR",
        "place": "Мозырь",
        "responsibilities": "Приемка товаров. Работа со складом. Выдача заказов покупателям. Оформление возвратов. "
        "Поддержание пункта в чистоте и порядке.",
        "url": "https://hh.ru/vacancy/107217584",
    }
