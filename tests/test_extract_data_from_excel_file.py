import xlrd
from src import excel_file_processing
from itertools import product
from unittest.mock import patch

file = "files/test-input.xlsx"


# @patch('src.excel_file_processing._get_sheet_name_and_year')
def test_get_data_from_workbook():
    excel_file_processing.extract_data_from_file(file=file)
    excel_wb = xlrd.open_workbook(filename=file)
    first_sheet = excel_wb.sheet_by_index(0)
    with patch.object(
        excel_file_processing,
        "_get_sheet_name_and_year",
        return_value=("Lit 3", "2019-2020"),
    ) as _get_sheet_name_and_year_mock:
        excel_file_processing._get_sheet_name_and_year(sheet=first_sheet)

    _get_sheet_name_and_year_mock.assert_called()


def test_get_subject_name_and_year():
    excel_wb = xlrd.open_workbook(filename=file)
    first_sheet = excel_wb.sheet_by_index(0)

    stuff = excel_file_processing._get_sheet_name_and_year(sheet=first_sheet)

    assert stuff == ("Lit 3", "2019-2020")


def test_get_row_value():
    pass
