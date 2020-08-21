import os

from sqlalchemy import create_engine

from src import database_manager
from src.database_manager import SchoolDB, Student, Subject, StudentSubject


db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
connection_url = (
    f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
)
engine = create_engine(connection_url)
# Drop all table on the database before starting the tests
database_manager.Base.metadata.drop_all(engine)


school_data_manager = SchoolDB(
    db_name=db_name,
    db_user=db_user,
    db_pass=db_pass,
    db_host=db_host,
    db_port=db_port,
)


def test_student_on_db_false():
    with database_manager.session_scope(
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
        db_name=db_name,
    ) as session:
        result = school_data_manager._student_on_db(
            name="Tov", last_name="dsvsv", session=session
        )

    assert result is False


def test_new_student_Isa_created():
    with database_manager.session_scope(
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
        db_name=db_name,
    ) as session:
        school_data_manager._get_or_create_student(
            name="Isa", last_name="Garvi", session=session
        )

        result = session.query(Student).first()

        assert result.name == "Isa"


def test_student_on_db_true():
    with database_manager.session_scope(
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
        db_name=db_name,
    ) as session:

        result = school_data_manager._student_on_db(
            name="Isa", last_name="Garvi", session=session
        )

    assert result is True


def test_student_not_added_if_already_exists_in_db():
    with database_manager.session_scope(
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
        db_name=db_name,
    ) as session:
        school_data_manager._get_or_create_student(
            name="Isa", last_name="Garvi", session=session
        )

        result = (
            session.query(Student)
            .filter(Student.name == "Isa", Student.last_name == "Garvi")
            .count()
        )

        assert result == 1


def test_store_data_in_db():
    # TODO: query to see if they were added to the db
    school_data_manager.store_data_in_db(
        name="Tov",
        last_name="Rod",
        subject="Math 3",
        year="2019-2020",
        mark=9.9,
    )
    school_data_manager.store_data_in_db(
        name="Isa",
        last_name="Garvi",
        subject="Math 3",
        year="2019-2020",
        mark=2,
    )


def test_subject_not_added_if_already_exists_in_db():
    # TODO: query to see if they were added to the db
    school_data_manager.store_data_in_db(
        name="Mar",
        last_name="Sousa",
        subject="Math 3",
        year="2019-2020",
        mark=8.9,
    )
    school_data_manager.store_data_in_db(
        name="Isa",
        last_name="Garvi",
        subject="Literature 3",
        year="2019-2020",
        mark=3.9,
    )
    school_data_manager.store_data_in_db(
        name="Tov",
        last_name="Rod",
        subject="Science 3",
        year="2019-2020",
        mark=4.9,
    )
    school_data_manager.store_data_in_db(
        name="Isa",
        last_name="Garvi",
        subject="Literature 4",
        year="2020-2021",
        mark=6.9,
    )


def test_two_students_passed_math3_20192020():
    result = school_data_manager.get_number_passed_by_subject_and_year(
        subject="Math 3", year="2019-2020"
    )
    assert result == 2


def test_one_student_failed_lit3_20192020():
    result = school_data_manager.get_number_failed_by_subject_and_year(
        subject="Literature 3", year="2019-2020"
    )
    assert result == 1


def test_list_passed_subject():
    result = school_data_manager.get_list_passed_by_subject_and_year(
        subject="Math 3", year="2019-2020"
    )

    assert result[0] == "Tov Rod"
    assert result[1] == "Mar Sousa"


def test_list_failed_subject():
    result = school_data_manager.get_list_failed_by_subject_and_year(
        subject="Literature 3", year="2019-2020"
    )

    assert result[0] == "Isa Garvi"


def test_three_students_math3_20192020():
    result = school_data_manager.get_number_students_by_subject_and_year(
        subject="Math 3", year="2019-2020"
    )

    assert result == 3


def test_list_students_per_subject_in_year():
    result = school_data_manager.get_list_students_by_subject_and_year(
        subject="Math 3", year="2019-2020"
    )

    assert result[0] == "Tov Rod"
    assert result[1] == "Isa Garvi"
    assert result[2] == "Mar Sousa"


def test_get_list_subjects_by_year():
    result = school_data_manager.get_list_subjects_by_year(year="2019-2020")

    assert result[0] == "Math 3"
    assert result[1] == "Literature 3"
    assert result[2] == "Science 3"
    assert "Literature 4" not in result
