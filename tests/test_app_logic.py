import os

from src import app_logic
from unittest.mock import patch


@patch("src.database_manager.SchoolDB.get_number_failed_by_subject_and_year")
@patch("src.database_manager.SchoolDB.get_number_students_by_subject_and_year")
def test_get_percentage_failed(
    get_number_failed_by_subject_and_year_mock,
    get_number_students_by_subject_and_year_mock,
):
    app_logic.get_percentage_failed(subject="Math 3", year="2019-2020")
    get_number_failed_by_subject_and_year_mock.assert_called_once()
    get_number_students_by_subject_and_year_mock.assert_called_once()


@patch("src.database_manager.SchoolDB.get_number_passed_by_subject_and_year")
@patch("src.database_manager.SchoolDB.get_number_students_by_subject_and_year")
def test_get_percetage_passed(
    get_number_passed_by_subject_and_year_mock,
    get_number_students_by_subject_and_year_mock,
):
    app_logic.get_percentage_passed(subject="Math 3", year="2019-2020")
    get_number_passed_by_subject_and_year_mock.assert_called_once()
    get_number_students_by_subject_and_year_mock.assert_called_once()


@patch("src.database_manager.SchoolDB.get_list_students_by_subject_and_year")
def test_get_list_students_in_subject(
    get_list_students_by_subject_and_year_mock,
):
    app_logic.get_list_students_in_subject("Math 3", "2019-2020")
    get_list_students_by_subject_and_year_mock.assert_called_once()


@patch("src.database_manager.SchoolDB.get_number_students_by_subject_and_year")
def test_get_total_number_students_in_subject(
    get_number_students_by_subject_and_year_mock,
):
    app_logic.get_total_number_students_in_subject("Math 3", "2020-2021")
    get_number_students_by_subject_and_year_mock.assert_called_once()


@patch("src.database_manager.SchoolDB.get_list_subjects_by_year")
def test_get_list_subjects_in_year(get_list_subjects_by_year_mock):
    app_logic.get_list_subjects_in_year("2019-2020")
    get_list_subjects_by_year_mock.assert_called_once()


@patch("src.database_manager.SchoolDB.store_data_in_db")
def test_store_data_in_db_called(store_data_in_db_mock):
    student_data = [["Marina", "sdvsdv", 2.0], ["Pau", "Real", 4.0]]
    app_logic.store_student_data(
        subject_name="Lit 4", year="2019-2020", student_data=student_data
    )
    store_data_in_db_mock.assert_called()
