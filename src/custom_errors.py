class Error(Exception):
    """Base class for other exceptions"""

    pass


class NotAnExcelFileError(Error):
    """Raise when the input file is not an Excel file.

    Attributes:
        file (str): input file that caused the error.
    """

    def __init__(self, file):
        self._file = file

    def __str__(self):
        return f"The file {self._file} is not an Excel file"


class WrongOrderOfColumns(Error):
    """Raise when the order of the columns in the sheet is not correct.

    Attributes:
        sheet: sheet where the columns are not correctly named.
    """

    def __init__(self, sheet):
        self._sheet = sheet

    def __str__(self):
        return f"The order of the columns on sheet {self._sheet} is incorrect.\n \
            It should be Name-Last name-Mark."


class WrongSheetName(Error):
    """Raise when the name of the sheet is incorrect.

    Attributes:
        sheet: sheet that has the wrong name.
    """

    def __init__(self, sheet):
        self._sheet = sheet

    def __str__(self):
        return f"Name of sheet {self._sheet} is incorrect.\n \
            The name should be 'subject course year'"
