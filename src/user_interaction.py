import sys
import inquirer

from src import app_logic


class UserInteraction:
    def __init__(self):
        sys.stdout.write(f"WELCOME TO THE PROGRAM.\n")
        questions = [
            inquirer.List(
                "function",
                message="What data do you need?",
                choices=[
                    "Percentage of students that failed a subject",
                    "Percentage of students that passed a subject",
                    "Total number of students taking a subject",
                    "List of students in a subject",
                    "List of subjects in a year",
                ],
            ),
        ]

        selection = inquirer.prompt(questions)["function"]
        self._process_selection(selection=selection)

        # if selection is not "List of subjects in a year":
        #     sys.stdout.write(
        #         f"Please, input the subject from which you want to obtain the data"
        #     )
        #     subject_name = str(input())
        #
        #     result = self.get_result(
        #         selection=selection, year=year, subject=subject_name
        #     )
        # else:
        #     result = self.get_result(selection=selection, year=year)

    def _process_selection(self, selection: str):
        if selection == "Percentage of students that failed a subject":
            year = self._get_year_from_input()
            subject = self._get_subject_from_input()
            result = app_logic.get_percentage_failed(
                subject=subject, year=year
            )
        elif selection == "Percentage of students that passed a subject":
            year = self._get_year_from_input()
            subject = self._get_subject_from_input()
            result = app_logic.get_percentage_passed(
                subject=subject, year=year
            )
        elif selection == "Total number of students taking a subject":
            year = self._get_year_from_input()
            subject = self._get_subject_from_input()
            result = app_logic.get_total_number_students_in_subject(
                subject=subject, year=year
            )
        elif selection == "List of students in a subject":
            year = self._get_year_from_input()
            subject = self._get_subject_from_input()
            result = app_logic.get_list_students_in_subject(
                subject=subject, year=year
            )
        else:
            year = self._get_year_from_input()
            result = app_logic.get_list_subjects_in_year(year=year)

    def _get_year_from_input(self):
        sys.stdout.write(
            f"Please, input the year from which you want to obtain the data"
        )
        return str(input())

    def _get_subject_from_input(self):
        sys.stdout.write(
            f"Please, input the subject from which you want to obtain the data"
        )
        return str(input())

    # def get_result(self, selection: str, year: str, subject: str = None):
    #     switcher = {
    #         "Percentage of students that failed a subject": app_logic.get_percentage_failed(
    #             subject=subject, year=year
    #         ),
    #         "Percentage of students that passed a subject": app_logic.get_percentage_passed(
    #             subject=subject, year=year
    #         ),
    #         "Total number of students taking a subject": app_logic.get_total_number_students_in_subject(
    #             subject=subject, year=year
    #         ),
    #         "List of students in a subject": app_logic.get_list_students_in_subject(
    #             subject=subject, year=year
    #         ),
    #         "List of subjects in a year": app_logic.get_list_subjects_in_year(
    #             year=year
    #         ),
    #     }
    #
    #     return switcher.get(selection)
