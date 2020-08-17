from typing import List
import xlrd as xlrd


def get_workbook_from_excel_file(file) -> None:
    """
    Opens the file passed by parameter and processes it as an Excel file.
    Gets all the sheets in the Excel file.

    :param file: file to be processed
    """

    return xlrd.open_workbook(filename=file)


def get_data_from_workbook(workbook):
    sheet_name_and_year = []

    for sheet in workbook.sheets():
        sheet_name_and_year.append(get_sheet_name_and_year(sheet))


def get_sheet_name_and_year(sheet) -> List[tuple]:
    subject, course, year = sheet.name.split()
    return subject + " " + course, year


def get_columns_name_from_sheet():
    pass
