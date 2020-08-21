import os
import sys
from typing import List

from src.database_manager import SchoolDB

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")


school_data_manager = SchoolDB(
    db_name=db_name,
    db_user=db_user,
    db_pass=db_pass,
    db_host=db_host,
    db_port=db_port,
)


def store_student_data(
    subject_name: str, year: str, student_data: List[list]
) -> None:
    """Call for storing the student data into the db for each element of student_data.

    Args:
        subject_name (str): name of the subject.
        year (str): year in which the subject has been taught.
        student_data (List[list]): Data of the students of that subject on that given year.
    """
    for student in student_data:
        school_data_manager.store_data_in_db(
            name=student[0],
            last_name=student[1],
            mark=student[2],
            subject=subject_name,
            year=year,
        )


def get_percentage_failed(subject: str, year: str) -> float:
    """Calculate the percentage of students that failed a subject on a given year getting the data from the database.

    Args:
        subject (str): Name of the subject to get the information from.
        year (str): Year in which the subject was taught.

    Returns:
        float: Percentage of students that failed the subject on year passed as a parameter.
    """
    failed = school_data_manager.get_number_failed_by_subject_and_year(
        subject=subject, year=year
    )
    total = school_data_manager.get_number_students_by_subject_and_year(
        subject=subject, year=year
    )

    try:
        percentage = float(failed / total)

        return percentage
    except ZeroDivisionError:
        sys.stderr.write(f"We do not have data for the pairing subject-year.")


def get_percentage_passed(subject: str, year: str) -> float:
    """Calculate the percentage of students that passed a subject on a given year getting the data from the database.

    Args:
        subject (str): Name of the subject to get the information from.
        year (str): Year in which the subject was taught.

    Returns:
        float: Percentage of students that passed the subject on year passed as a parameter.
    """
    passed = school_data_manager.get_number_passed_by_subject_and_year(
        subject=subject, year=year
    )
    total = school_data_manager.get_number_students_by_subject_and_year(
        subject=subject, year=year
    )

    try:
        percentage = float(passed / total)

        return percentage
    except ZeroDivisionError:
        sys.stderr.write(f"We do not have data for the pairing subject-year.")


def get_list_students_in_subject(subject: str, year: str) -> List[str]:
    """Get a list of students that were enrolled in a subject on a given year.

    Args:
        subject (str): Name of the subject to get the information from.
        year (str): Year in which the subject was taught.

    Returns:
        List[str]: List of students' name and last name that were enrolled in the subject on year passed.
    """
    return school_data_manager.get_list_students_by_subject_and_year(
        subject=subject, year=year
    )


def get_total_number_students_in_subject(subject: str, year: str) -> int:
    """Get the total number of students that were enrolled in a subject on a given year.

    Args:
        subject (str): Name of the subject to get the information from.
        year (str): Year in which the subject was taught.

    Returns:
        int: Total number of students enrolled in the subject on the year passed as a parameter.
    """
    return school_data_manager.get_number_students_by_subject_and_year(
        subject=subject, year=year
    )


def get_list_subjects_in_year(year: str) -> List[str]:
    """Get the list of subject taught in a given year.

    Args:
        year (str): Year from which we want the information.

    Returns:
        List[str]: Subjects that where taught in the year passed as parameter.
    """
    return school_data_manager.get_list_subjects_by_year(year=year)
