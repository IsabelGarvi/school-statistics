# School Statistics
With this program we will be able to know the percentage of students that have
passed a subject, or that haven't, as well as obtaining the list of names of 
students that have passed, that have not passed or that are enrolled in a subject.
We will be able to also know the subjects a student is enrolled in. 

We receive an input file (en Excel file), process it and we will be ask about actions
in the console. 

We will receive the answers also in the console (if we want we can pipe to an
output file).

The input file will have the columns:
- Name of the student
- Last name of the student
- Retake (this lets us know if the student retook the exam because he had failed or not)
- Mark
- Year

Retake column cannot be ticked if there is no retake column empty for that 
same student on that same subject and that same year.
Ideally -> 1 excel sheet for each subject.
