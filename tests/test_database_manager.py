import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
Session = sessionmaker(engine)

school_data_manager = SchoolDB(
    db_name=db_name,
    db_user=db_user,
    db_pass=db_pass,
    db_host=db_host,
    db_port=db_port,
)


def test_student_on_db_false():
    session = Session()
    result = school_data_manager._student_on_db(
        name="Tov", last_name="dsvsv", session=session
    )

    assert result is False


def test_create_new_student():
    session = Session()

    school_data_manager._get_or_create_student(
        name="Isa", last_name="Garvi", session=session
    )

    result = session.query(Student).first()

    assert result.name == "Isa"
