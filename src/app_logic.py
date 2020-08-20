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


def store_student_data(subject_name, year, student_data) -> None:
    for student in student_data:
        school_data_manager.store_data_in_db(
            name=student[0],
            last_name=student[1],
            mark=student[2],
            subject=subject_name,
            year=year,
        )


def get_percentage_failed(subject: str, year: str) -> float:
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
        print("failed")
        sys.stderr.write(f"We do not have data for the pairing subject-year.")


def get_percentage_passed(subject: str, year: str) -> float:
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
        print("passed")
        sys.stderr.write(f"We do not have data for the pairing subject-year.")


def get_list_students_in_subject(subject: str, year: str) -> List[str]:
    return school_data_manager.get_list_students_by_subject_and_year(
        subject=subject, year=year
    )


def get_total_number_students_in_subject(subject: str, year: str) -> int:
    return school_data_manager.get_number_students_by_subject_and_year(
        subject=subject, year=year
    )


def get_list_subjects_in_year(year: str) -> List[str]:
    return school_data_manager.get_list_subjects_by_year(year=year)
