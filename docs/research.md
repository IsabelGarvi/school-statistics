# Research    
###  Pandas vs xlrd
Pandas uses xlrd on a lower level to read the excel file, but is much more powerful
than xlrd. We're going to use pandas in this project.

`wb = pd.ExcelFile(excel_file)` reads all the data in an Excel file, which is useful 
if we have more than one sheet.

We can then load each sheet using `df = pd.read_excel(file_name, sheetname="house")`

`wb.sheet_names` gets us the names of all the sheets in a list. To know
the total number of sheets we'll use `len(wb.sheet_names)`

If we want the info for each of the sheet we will do:
`for sheet in xlsx.sheet_names:
   wb.parse(sheet)`
   
This means we are going to process each sheet separately as if each one of them
were a different file.

