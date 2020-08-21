import sys
from typing import List

import inquirer

from src import app_logic


def user_interaction():
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

    year = _get_year_from_input()

    if selection != "List of subjects in a year":
        sys.stdout.write(
            f"Please, input the subject from which you want to obtain the data\n"
        )
        subject_name = str(input())

        result = _process_selection(
            selection=selection, year=year, subject=subject_name
        )
    else:
        result = _process_selection(selection=selection, year=year)

    _process_and_print_result(result=result)


def _get_year_from_input():
    sys.stdout.write(
        f"Please, input the year from which you want to obtain the data\n"
    )
    return str(input())


def _get_subject_from_input():
    sys.stdout.write(
        f"Please, input the subject from which you want to obtain the data\n"
    )
    return str(input())


# TODO: more efficient way of handling the choice?
def _process_selection(selection: str, year: str, subject: str = None):
    if selection == "Percentage of students that failed a subject":
        return app_logic.get_percentage_failed(subject=subject, year=year)
    elif selection == "Percentage of students that passed a subject":
        return app_logic.get_percentage_passed(subject=subject, year=year)
    elif selection == "Total number of students taking a subject":
        return app_logic.get_total_number_students_in_subject(
            subject=subject, year=year
        )
    elif selection == "List of students in a subject":
        return app_logic.get_list_students_in_subject(
            subject=subject, year=year
        )
    else:
        return app_logic.get_list_subjects_in_year(year=year)


def _process_and_print_result(result: [int, List]):
    if type(result) is int or type(result) is float:
        sys.stdout.write(f"This is the result of your question: {result}\n")
    elif type(result) is list:
        sys.stdout.write(f"This is the result of the search:\n")
        if len(result) == 0:
            sys.stdout.write(f"none.")
        else:
            for element in result:
                sys.stdout.write(f"{element}\n")
