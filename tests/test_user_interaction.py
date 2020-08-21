from src import user_interaction
from unittest.mock import patch


@patch("src.app_logic.get_percentage_failed")
def test_percentage_of_failed_students_function_called(
    get_percentage_failed_mock,
):
    user_interaction._process_selection(
        selection="Percentage of students that failed a subject",
        subject="Lit 4",
        year="2019-2020",
    )
    get_percentage_failed_mock.assert_called_once()


@patch("src.app_logic.get_percentage_passed")
def test_percentage_of_passed_students_function_called(
    get_percentage_passed_mock,
):
    user_interaction._process_selection(
        selection="Percentage of students that passed a subject",
        subject="Lit 4",
        year="2019-2020",
    )
    get_percentage_passed_mock.assert_called_once()


@patch("src.app_logic.get_total_number_students_in_subject")
def test_total_number_of_students_function_called(
    get_total_number_students_in_subject_mock,
):
    user_interaction._process_selection(
        selection="Total number of students taking a subject",
        subject="Lit 4",
        year="2019-2020",
    )
    get_total_number_students_in_subject_mock.assert_called_once()


@patch("src.app_logic.get_list_students_in_subject")
def test_list_of_students_function_called(get_list_students_in_subject_mock):
    user_interaction._process_selection(
        selection="List of students in a subject",
        subject="Lit 4",
        year="2019-2020",
    )
    get_list_students_in_subject_mock.assert_called_once()


@patch("src.app_logic.get_list_subjects_in_year")
def test_list_of_subjects_function_called(get_list_subjects_in_year_mock):
    user_interaction._process_selection(
        selection="List of subjects in a year", year="2019-2020"
    )
    get_list_subjects_in_year_mock.assert_called_once()
