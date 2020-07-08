import xlrd as xlrd


def process_excel_file(file) -> None:
    """
    Opens the file passed by parameter and processes it as an Excel file.
    Gets all the sheets in the Excel file.

    :param file: file to be processed
    """
    excel_file = open(file, "+r")

    wb = xlrd.open_workbook(excel_file)
    sheets = wb.sheets()
