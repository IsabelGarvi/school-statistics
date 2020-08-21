import xlrd
import pytest
from src import excel_file_processing
from itertools import product
from unittest.mock import patch
from src.custom_errors import NotAnExcelFileError, WrongOrderOfColumns

input_file = "files/test-input.xlsx"
invalid_columns_file = "files/test-input-invalid-columns.xlsx"
not_excel_file = "files/no-excel-file-test.txt"


def test_input_file_not_valid():
    result = excel_file_processing._is_excel_file(file=not_excel_file)
    assert result is False


def test_input_file_valid():
    result = excel_file_processing._is_excel_file(file=input_file)
    assert result is True


def test_column_order_valid():
    excel_wb = xlrd.open_workbook(filename=input_file)
    first_sheet = excel_wb.sheet_by_index(0)

    result = excel_file_processing._validate_column_order(sheet=first_sheet)
    assert result is True


def test_column_order_not_valid():
    excel_wb = xlrd.open_workbook(filename=invalid_columns_file)
    first_sheet = excel_wb.sheet_by_index(0)

    result = excel_file_processing._validate_column_order(sheet=first_sheet)
    assert result is False


def test_invalid_column_order_error():
    with pytest.raises(WrongOrderOfColumns):
        excel_file_processing.extract_data_from_file(file=invalid_columns_file)


def test_get_subject_name_and_year_called():
    with patch.object(
        excel_file_processing,
        "_get_subject_name_and_year",
        return_value=("Lit 3", "2019-2020"),
    ) as _get_subject_name_and_year_mock:
        excel_file_processing.extract_data_from_file(file=input_file)

    _get_subject_name_and_year_mock.assert_called()


def test_not_an_excel_file_error():
    with pytest.raises(NotAnExcelFileError):
        excel_file_processing.extract_data_from_file(file=not_excel_file)


def test_first_sheet_name_lit3_year20192020():
    excel_wb = xlrd.open_workbook(filename=input_file)
    first_sheet = excel_wb.sheet_by_index(0)

    subject_name_and_year = excel_file_processing._get_subject_name_and_year(
        sheet=first_sheet
    )

    assert subject_name_and_year == ("Lit 3", "2019-2020")


def test_first_student_data_from_Lit3_20192020():
    excel_wb = xlrd.open_workbook(filename=input_file)
    first_sheet = excel_wb.sheet_by_index(0)

    student_data = excel_file_processing._get_row_data_from_sheet(
        sheet=first_sheet
    )

    assert student_data[0] == ["Isa", "Garvi", 9.0]


def test_students_data_length_is_five():
    excel_wb = xlrd.open_workbook(filename=input_file)
    first_sheet = excel_wb.sheet_by_index(0)

    student_data = excel_file_processing._get_row_data_from_sheet(
        sheet=first_sheet
    )

    assert len(student_data) == 5
