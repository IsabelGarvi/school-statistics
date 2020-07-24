import sys
from typing import List

from src.database_manager import SchoolDB


def get_percentage_failed(subject: str, year: str) -> float:
    failed = SchoolDB.get_number_failed_by_subject_and_year(
        subject=subject, year=year
    )
    total = SchoolDB.get_number_students_by_subject_and_year(
        subject=subject, year=year
    )

    percentage = float(failed / total)

    # sys.stdout.write(f'The percentage of students that failed the subject {subject} in year {year} is {percentage}% ')

    return percentage


def get_percentage_passed(subject: str, year: str) -> float:
    passed = SchoolDB.get_number_passed_by_subject_and_year(
        subject=subject, year=year
    )
    total = SchoolDB.get_number_students_by_subject_and_year(
        subject=subject, year=year
    )

    percentage = float(passed / total)

    # sys.stdout.write(f'The percentage of students that passed the subject {subject} in year {year} is {percentage}% ')

    return percentage


def get_list_students_in_subject(subject: str, year: str) -> List[str]:
    return SchoolDB.get_list_students_by_subject_and_year(
        subject=subject, year=year
    )

    # sys.stdout.write(f'This is the list of students for the subject {subject} in year {year}:')
    #
    # for student in students:
    #     sys.stdout.write(f'{student}')


def get_total_number_students_in_subject(subject: str, year: str) -> int:
    return SchoolDB.get_number_students_by_subject_and_year(
        subject=subject, year=year
    )


def get_list_subjects_in_year(year: str) -> List[str]:
    return SchoolDB.get_list_subjects_by_year(year=year)

    # sys.stdout.write(f'This is the list of subjects in year {year}:')
    #
    # for subject in subjects:
    #     sys.stdout.write(f'{subject}')
