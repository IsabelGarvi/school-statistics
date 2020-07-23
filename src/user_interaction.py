import sys
import inquirer


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
                    "List of students in a year",
                    "List of subjects in a year",
                ],
            ),
        ]
        answers = inquirer.prompt(questions)
