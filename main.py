from src.hh_vacancies_api import HHVacanciesApi
from src.json_processor import JSONProcessor
from src.utils import filter_by_place, filter_by_word, sort_by_salary


def user_interaction():
    """Функция для взаимодействия с пользователем."""
    hh = HHVacanciesApi()

    user_input = input("Введите запрос для поиска на сайте вакансий: ")
    vacancies = hh.get_vacancies(user_input)
    print(f"\nПо вашему запросу найдено {len(vacancies)} вакансий.")

    user_input = input(
        "\nДля записи вакансий в файл введите имя файла или нажмите Enter " "для записи в файл по умолчанию: "
    )
    JSONProcessor(vacancies, user_input)

    user_input = input("\nХотите отфильтровать вакансии по определенным словам в описании (да/нет): ").strip().lower()
    if user_input == "да":
        user_input = input("\nВведите ключевое/ые слово/а для фильтрации вакансий через запятую или пробел: ")
        user_input = user_input.replace(",", " ").replace("  ", " ").split()
        print(user_input)
        vacancies = filter_by_word(vacancies, user_input)

    user_input = input("\nХотите отфильтровать вакансии по определенной/ому стране/городу (да/нет): ").strip().lower()
    if user_input == "да":
        user_input = input("\nВведите название страны/города для фильтрации вакансий: ")
        vacancies = filter_by_place(vacancies, user_input)

    print(f"\nКоличество отфильтрованных вакансий: {len(vacancies)}")
    user_input = int(
        input(
            f"\nВведите число для вывода топ-n по зарплатам "
            f"(число должно быть больше 1 и меньше {len(vacancies)}): "
        )
    )
    print(sort_by_salary(vacancies, user_input))


if __name__ == "__main__":
    user_interaction()
