import xlrd
from src import excel_file_processing

file = "files/test-input.xlsx"


def test_get_data_from_workbook():
    excel_wb = xlrd.open_workbook(filename=file)
    pass


def test_get_subject_name_and_year():
    excel_wb = xlrd.open_workbook(filename=file)
    first_sheet = excel_wb.sheet_by_index(0)

    stuff = excel_file_processing.get_sheet_name_and_year(sheet=first_sheet)

    assert stuff == ("Lit 3", "2019-2020")


# def test_get_column_value():
#     excel_wb = xlrd.open_workbook(filename=file)
#     for sheet in excel_wb.sheets():
#         print(sheet.col_values(columnindex))
