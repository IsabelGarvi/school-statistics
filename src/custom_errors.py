class Error(Exception):
    """Base class for other exceptions"""

    pass


class NotAnExcelFileError(Error):
    """Raise when the input file is not an Excel file.

    Attributes:
        file: input file that caused the error.
    """

    def __init__(self, file):
        self._file = file

    def __str__(self):
        return f"The file {self._file} is not an Excel file"
