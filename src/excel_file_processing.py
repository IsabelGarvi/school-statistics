import xlrd as xlrd


def get_workbook_from_excel_file(file) -> None:
    """
    Opens the file passed by parameter and processes it as an Excel file.
    Gets all the sheets in the Excel file.

    :param file: file to be processed
    """
    excel_file = open(file, "+r")

    return xlrd.open_workbook(excel_file)


def get_sheets_from_workbook(workbook):
    return workbook.sheets()


def get_columns_name_from_sheet():
    pass
