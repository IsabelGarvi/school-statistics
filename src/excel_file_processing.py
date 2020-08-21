from typing import List
import xlrd as xlrd
import os
import sys
import functools
from src.app_logic import store_student_data
from src.custom_errors import (
    NotAnExcelFileError,
    WrongOrderOfColumns,
    WrongSheetName,
)


def extract_data_from_file(file: str) -> None:
    """Extract the data from the file and call for store in the database.

    Args:
        file (str): path to the file which the data is going to be extracted from.

    Raises:
        WrongOrderOfColumns: Error raised when the order of the columns of the sheet is not valid.
        NotAnExcelFileError: Error raised when the file is not an excel file.
    """
    if _is_excel_file(file=file):
        workbook = xlrd.open_workbook(filename=file)
        for sheet in workbook.sheets():
            subject_name, year = _get_subject_name_and_year(sheet=sheet)
            if _validate_column_order(sheet=sheet):
                student_data = _get_row_data_from_sheet(sheet=sheet)
                store_student_data(
                    subject_name=subject_name,
                    year=year,
                    student_data=student_data,
                )
            else:
                raise WrongOrderOfColumns(sheet=sheet)
    else:
        raise NotAnExcelFileError(file=file)


def _is_excel_file(file: str) -> bool:
    """Get the extension of the file and check if it corresponds to an excel file.

    Args:
        file (str): path of the file to be examined.

    Returns:
        bool: Whether the file is an excel file.
    """
    filename, file_extension = os.path.splitext(file)
    if file_extension == ".xls" or file_extension == ".xlsx":
        return True
    else:
        return False


def _validate_column_order(sheet: xlrd.sheet.Sheet) -> bool:
    """Check if the order of the columns in the sheet is the one we want.

    Args:
        sheet (xlrd.sheet.Sheet): Sheet to be examined.

    Returns:
        bool: Whether the order of the columns is valid.
    """
    header = sheet.row_values(0)
    if header == ["Name", "Last name", "Mark"]:
        return True
    else:
        return False


# TODO: test raise Error
def _get_subject_name_and_year(sheet: xlrd.sheet.Sheet) -> tuple:
    """Get the name of the sheet and obtain the subject name and year.

    Args:
        sheet (xlrd.sheet.Sheet): Sheet from where we are getting the name.

    Raises:
        WrongSheetName: Error raised when the name of the sheet is not valid.

    Returns:
        tuple: name of the subject and year.
    """
    splitted_name = sheet.name.split()
    if _validate_length_of_sheet_name:
        year = splitted_name[-1]
        course = splitted_name[-2]
        subject = splitted_name[:-2]

        subject_name = subject[0] if len(subject) == 1 else " ".join(subject)
        full_subject_name = subject_name + " " + course
    else:
        raise WrongSheetName(sheet=sheet)

    return full_subject_name, year


# TODO: test this function for both outcomes
def _validate_length_of_sheet_name(splitted_name: List) -> bool:
    """Validate if the length of the sheet name is equal or greater than three.

    Args:
        splitted_name (List): Contains the elements of the sheet name.

    Returns:
        bool: Whether the length of the list is equal or greater than three.
    """
    return True if len(splitted_name) >= 3 else False


# TODO: format the year string
def _format_year(year: str) -> str:
    """Format the year obtained from the sheet name to the format that we want to insert into the database.
    That format is XXXX-XXXX.

    Args:
        year (str): String to be formatted.

    Returns:
        str: Formatted string.
    """
    pass


def _get_row_data_from_sheet(sheet: xlrd.sheet.Sheet) -> List[list]:
    """Get value from each row of the sheet passed by parameter and append it to a list.

    Args:
        sheet (xlrd.sheet.Sheet): Sheet from the workbook to get the info.

    Returns:
        List[list]: List of lists where each element is the data of a student.
    """
    student_data = []
    for row_index in range(1, sheet.nrows):
        student_data.append(sheet.row_values(row_index))

    return student_data
