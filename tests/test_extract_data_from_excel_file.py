import xlrd
from src import excel_file_processing
from itertools import product
from unittest.mock import patch

file = "files/test-input.xlsx"


def test_get_sheet_name_and_year_called():
    with patch.object(
        excel_file_processing,
        "_get_sheet_name_and_year",
        return_value=("Lit 3", "2019-2020"),
    ) as _get_sheet_name_and_year_mock:
        excel_file_processing.extract_data_from_file(file=file)

    _get_sheet_name_and_year_mock.assert_called()


def test_first_sheet_name_lit3_year20192020():
    excel_wb = xlrd.open_workbook(filename=file)
    first_sheet = excel_wb.sheet_by_index(0)

    subject_name_and_year = excel_file_processing._get_sheet_name_and_year(
        sheet=first_sheet
    )

    assert subject_name_and_year == ("Lit 3", "2019-2020")


def test_first_student_data_from_Lit3_20192020():
    excel_wb = xlrd.open_workbook(filename=file)
    first_sheet = excel_wb.sheet_by_index(0)

    student_data = excel_file_processing._get_row_data_from_sheet(
        sheet=first_sheet
    )

    assert student_data[0] == ["Isa", "Garvi", 9.0]


def test_students_data_length_is_five():
    excel_wb = xlrd.open_workbook(filename=file)
    first_sheet = excel_wb.sheet_by_index(0)

    student_data = excel_file_processing._get_row_data_from_sheet(
        sheet=first_sheet
    )

    assert len(student_data) == 5
