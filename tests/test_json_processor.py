from unittest.mock import PropertyMock, mock_open, patch

import pytest

from src.json_processor import JSONProcessor


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.dirname", return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("src.json_processor.json.dump")
def test_json_processor_init(mock_json, mock_join, mock_dirname, mock_opened, vacancies_list):
    """Тестирует инициализацию объектов класса."""
    json_processor = JSONProcessor(vacancies_list)

    assert len(json_processor.__dict__) == 3

    mock_json.assert_called_once_with(
        vacancies_list,
        mock_opened("/mock/path/data/vacancies.json", "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )
    mock_opened.assert_called_with("/mock/path/data/vacancies.json", "w", encoding="utf-8")


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.dirname", return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("src.json_processor.json.dump")
def test_json_processor_init_file_name(mock_json, mock_join, mock_dirname, mock_opened, vacancies_list):
    """Тестирует инициализацию объектов класса с переданным именем файла."""
    JSONProcessor(vacancies_list, "some_file.json")

    mock_json.assert_called_once_with(
        vacancies_list,
        mock_opened("/mock/path/data/some_file.json", "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )
    mock_opened.assert_called_with("/mock/path/data/some_file.json", "w", encoding="utf-8")


@pytest.mark.parametrize("file_name", ["file.not_json", "some_file.xlsx", "some_file.csv", "some_file.txt"])
def test_json_processor_init_wrong_file_name(file_name, vacancies_list):
    """Тестирует инициализацию объектов класса при передаче неверного имени файла."""
    with pytest.raises(ValueError, match="Класс предназначен для работы с JSON-файлами."):
        JSONProcessor(vacancies_list, file_name)


def test_json_processor_init_wrong_vacancies_not_a_list(vacancy_1):
    """Тестирует инициализацию объектов класса при передаче неверных данных для записи (не список)."""
    with pytest.raises(ValueError, match="Данные должны передаваться в виде списка словарей."):
        JSONProcessor(vacancy_1)


def test_json_processor_init_wrong_vacancies_empty_list(vacancy_1, vacancy_2):
    """Тестирует инициализацию объектов класса при передаче неверных данных для записи (не словари)."""
    with pytest.raises(ValueError, match="Данные должны передаваться в виде списка словарей."):
        JSONProcessor([vacancy_1, vacancy_2])


def test_json_processor_init_wrong_vacancies_wrong_keys(vacancy_dict):
    """Тестирует инициализацию объектов класса при передаче неверных данных для записи (неправильные ключи)."""
    vacancy_dict.pop("url")
    with pytest.raises(ValueError, match=f"Данные {vacancy_dict} должны соответствовать атрибутам класса Vacancy."):
        JSONProcessor([vacancy_dict])


@patch("src.json_processor.open")
@patch.object(JSONProcessor, "_JSONProcessor__BASE_PATH", new_callable=PropertyMock, return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("src.json_processor.json.load")
def test_json_processor_get_data(mock_json_load, mock_join, mock_path, mock_open, vacancies_list):
    """Тестирует получение данных из файла."""
    json_processor = JSONProcessor(vacancies_list)
    mock_json_load.return_value = vacancies_list

    assert json_processor.get_data() == vacancies_list
    mock_open.assert_called_with("/mock/path/vacancies.json", encoding="utf-8")


@patch("builtins.open", new_callable=mock_open)
@patch.object(JSONProcessor, "_JSONProcessor__BASE_PATH", new_callable=PropertyMock, return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("src.json_processor.json.dump")
@patch("src.json_processor.JSONProcessor.get_data")
def test_json_processor_add_data(
    mock_get_data, mock_json_dump, mock_join, mock_path, mock_open, vacancies_list, vacancy_dict
):
    """Тестирует добавление новых данных в файл."""
    json_processor = JSONProcessor(vacancies_list)
    mock_get_data.return_value = vacancies_list
    json_processor.add_data(vacancy_dict)

    vacancies_list.append(vacancy_dict)
    mock_json_dump.assert_called_with(
        vacancies_list,
        mock_open("/mock/path/vacancies.json", "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )


@patch("builtins.open", new_callable=mock_open)
@patch.object(JSONProcessor, "_JSONProcessor__BASE_PATH", new_callable=PropertyMock, return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("src.json_processor.json.dump")
@patch("src.json_processor.JSONProcessor.get_data")
def test_json_processor_add_data_existing_data(
    mock_get_data, mock_json_dump, mock_join, mock_path, mock_open, vacancies_list
):
    """Тестирует работу метода при добавлении существующих данных."""
    json_processor = JSONProcessor(vacancies_list)
    mock_get_data.return_value = vacancies_list
    json_processor.add_data(vacancies_list[0])

    mock_json_dump.assert_called_with(
        vacancies_list,
        mock_open("/mock/path/vacancies.json", "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )


@patch("builtins.open", new_callable=mock_open)
@patch.object(JSONProcessor, "_JSONProcessor__BASE_PATH", new_callable=PropertyMock, return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("src.json_processor.json.dump")
def test_json_processor_add_data_wrong_data(
    mock_json_dump, mock_join, mock_path, mock_open, vacancies_list, vacancy_1, vacancy_dict
):
    """Тестирует работу метода при добавлении неверных данных."""
    json_processor = JSONProcessor(vacancies_list)
    with pytest.raises(ValueError, match=f"Данные {vacancy_1} должны передаваться в виде словаря."):
        json_processor.add_data(vacancy_1)

    vacancy_dict.pop("url")
    with pytest.raises(ValueError, match=f"Данные {vacancy_dict} должны соответствовать атрибутам класса Vacancy."):
        json_processor.add_data(vacancy_dict)


@patch("builtins.open", new_callable=mock_open)
@patch.object(JSONProcessor, "_JSONProcessor__BASE_PATH", new_callable=PropertyMock, return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("src.json_processor.json.dump")
@patch("src.json_processor.JSONProcessor.get_data")
def test_json_processor_delete_data(mock_get_data, mock_json_dump, mock_join, mock_path, mock_open, vacancies_list):
    """Тестирует удаление заданной вакансии из файла."""
    json_processor = JSONProcessor(vacancies_list)
    mock_get_data.return_value = vacancies_list
    json_processor.delete_data(vacancies_list[0])

    mock_json_dump.assert_called_with(
        [vacancies_list[-1]],
        mock_open("/mock/path/vacancies.json", "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )


@patch("builtins.open", new_callable=mock_open)
@patch.object(JSONProcessor, "_JSONProcessor__BASE_PATH", new_callable=PropertyMock, return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("src.json_processor.json.dump")
def test_json_processor_delete_data_not_existing_vacancy(
    mock_json_dump, mock_join, mock_path, mock_open, vacancies_list, vacancy_dict
):
    """Тестирует удаление несуществующей вакансии."""
    json_processor = JSONProcessor(vacancies_list)
    with pytest.raises(ValueError, match="Вакансия с номером 107217584 отсутствует в файле и не может быть удалена."):
        json_processor.delete_data(vacancy_dict)


@patch("builtins.open", new_callable=mock_open)
@patch.object(JSONProcessor, "_JSONProcessor__BASE_PATH", new_callable=PropertyMock, return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("src.json_processor.json.dump")
def test_json_processor_delete_data_wrong_data(
    mock_json_dump, mock_join, mock_path, mock_open, vacancies_list, vacancy_1, vacancy_dict
):
    """Тестирует работу метода при удалении неверных данных."""
    json_processor = JSONProcessor(vacancies_list)
    with pytest.raises(ValueError, match=f"Данные {vacancy_1} должны передаваться в виде словаря."):
        json_processor.add_data(vacancy_1)

    vacancy_dict.pop("url")
    with pytest.raises(ValueError, match=f"Данные {vacancy_dict} должны соответствовать атрибутам класса Vacancy."):
        json_processor.add_data(vacancy_dict)
