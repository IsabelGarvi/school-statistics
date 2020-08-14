import xlrd
import pandas as pd

file = "files/test-input.xlsx"


def test_data():
    # excel_file = open("files/test-input.xlsx", "+r")

    wb = pd.ExcelFile(file)
    sheets = wb.sheet_names
    # Get the names of the sheets (subjects) to store in the db with wb.sheet_names()
    # Get the Columns names of each sheet with
    # for sheet in sheets:
    #     sheet.row_values(0) -> we assume the row(0) is the columns name. We need to check
    # this though
    print(f"Sheets names: {sheets}")

    # for sheet in sheets:
    # subject = wb.parse(sheet)
    # print(subject.columns.values)
    # print(subject.rows.values)

    pass
