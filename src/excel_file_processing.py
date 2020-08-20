from typing import List
import xlrd as xlrd


def extract_data_from_file(file) -> tuple:
    workbook = xlrd.open_workbook(filename=file)
    for sheet in workbook.sheets():
        subject_name, year = _get_sheet_name_and_year(sheet=sheet)
        student_data = _get_row_data_from_sheet(sheet=sheet)

    return subject_name, year, student_data


def _get_sheet_name_and_year(sheet) -> tuple:
    subject, course, year = sheet.name.split()
    return subject + " " + course, year


def _get_row_data_from_sheet(sheet) -> List[list]:
    student_data = []
    for row_index in range(1, sheet.nrows):
        student_data.append(sheet.row_values(row_index))

    return student_data
