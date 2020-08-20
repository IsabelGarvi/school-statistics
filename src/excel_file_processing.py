from typing import List
import xlrd as xlrd


def extract_data_from_file(file):
    workbook = xlrd.open_workbook(filename=file)
    for sheet in workbook.sheets():
        subject_name, year = _get_sheet_name_and_year(sheet=sheet)
    pass


def _get_sheet_name_and_year(sheet) -> tuple:
    subject, course, year = sheet.name.split()
    return subject + " " + course, year


def _get_row_data_from_sheet(sheet):
    for row_index in range(1, sheet.nrows):
        row_values = sheet.row_values(row_index)
        print(row_values)
