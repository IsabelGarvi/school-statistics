from typing import List
import xlrd as xlrd
import os
from src.app_logic import store_student_data


def _is_excel_file(file) -> bool:
    filename, file_extension = os.path.splitext(file)
    if file_extension == ".xls" or file_extension == ".xlsx":
        return True
    else:
        return False


def extract_data_from_file(file) -> None:
    if _is_excel_file(file=file):
        workbook = xlrd.open_workbook(filename=file)
        for sheet in workbook.sheets():
            subject_name, year = _get_sheet_name_and_year(sheet=sheet)
            student_data = _get_row_data_from_sheet(sheet=sheet)
            store_student_data(
                subject_name=subject_name, year=year, student_data=student_data
            )
    else:
        raise FileNotFoundError


def _get_sheet_name_and_year(sheet) -> tuple:
    subject, course, year = sheet.name.split()
    return subject + " " + course, year


def _get_row_data_from_sheet(sheet) -> List[list]:
    student_data = []
    for row_index in range(1, sheet.nrows):
        student_data.append(sheet.row_values(row_index))

    return student_data
