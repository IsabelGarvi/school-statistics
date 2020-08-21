import sys
from typing import List
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

Base = declarative_base()


class StudentSubject(Base):
    __tablename__ = "student_subject"
    subject_id = Column(
        Integer, ForeignKey("subject.id"), primary_key=True, nullable=False
    )
    student_id = Column(
        Integer, ForeignKey("student.id"), primary_key=True, nullable=False
    )
    mark = Column(Float)
    subject = relationship(
        "Subject",  # back_populates='students', cascade='all, delete',
    )


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String(50))
    last_name = Column(String(50))
    subjects = relationship(
        "StudentSubject",  # back_populates='subject', cascade='all, delete',
    )


class Subject(Base):
    __tablename__ = "subject"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String(50))
    natural_year = Column(
        String(50)
    )  # year in which the subject is taken (p.e. 2019-2020)


@contextmanager
def session_scope(user, password, host, port, db_name):
    """Provide a transactional scope around a series of operations."""
    connection_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(connection_url)
    Session = sessionmaker(engine)
    session = Session()
    Base.metadata.create_all(engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class SchoolDB:
    """Class to do all the operations on the database.

        Attributes:
            db_user (str): username of the database.
            db_pass (str): password for the database.
            db_host (str): host to connect to the database.
            db_port (str): port to connect to the database.
            db_name (str): name of the database to conect to.
    """

    def __init__(self, db_user, db_pass, db_host, db_port, db_name):
        self._user = db_user
        self._password = db_pass
        self._host = db_host
        self._port = db_port
        self._db_name = db_name

    def _get_or_create_student(
        self,
        name: str,
        last_name: str,
        session: sqlalchemy.orm.session.Session,
    ) -> Student:
        """Access to the student data on the db and created if it does not exist.

        Args:
            name (str): Name of the student  to be obtained/created.
            last_name (str): Last name of the student to be obtained/created.
            session (sqlalchemy.orm.session.Session): Session to connect to the db.

        Returns:
            Student: Student entry of the table, either the one obtained or the one created.
        """
        if not self._student_on_db(
            name=name, last_name=last_name, session=session
        ):
            new_student = Student(name=name, last_name=last_name)
            session.add(new_student)
        else:
            new_student = (
                session.query(Student)
                .filter(Student.name == name, Student.last_name == last_name)
                .first()
            )
        return new_student

    @staticmethod
    def _student_on_db(
        name: str, last_name: str, session: sqlalchemy.orm.session.Session
    ) -> bool:
        """Check if the student data is already in the db.

        Args:
            name (str): Name of the student to check.
            last_name (str): Last name of the student to check.
            session (sqlalchemy.orm.session.Session): Session to connect to the db.

        Returns:
            bool: Whether the data exists in the db.
        """
        return (
            session.query(Student)
            .filter(Student.name == name, Student.last_name == last_name)
            .count()
            != 0
        )

    def _get_or_create_subject(
        self, subject: str, year: str, session: sqlalchemy.orm.session.Session
    ) -> Subject:
        """Access to the subject data on the db and created if it does not exist.

        Args:
            subject (str): Name of the subject to be added to the db.
            year (str): Year to be able to check if the subject exists on the db.
            session (sqlalchemy.orm.session.Session): Session to connect to the db.

        Returns:
            Subject: Subject entry of the table, either created or obtained.
        """
        if not self._subject_on_db(
            subject=subject, year=year, session=session
        ):
            new_subject = Subject(name=subject, natural_year=year)
        else:
            new_subject = (
                session.query(Subject)
                .filter(Subject.name == subject, Subject.natural_year == year,)
                .first()
            )
        return new_subject

    @staticmethod
    def _subject_on_db(
        subject: str, year: str, session: sqlalchemy.orm.session.Session
    ) -> bool:
        """Check if the subject data is already in the db.

        Args:
            subject (str): Name of the subject to check.
            year (str): Year on which the subject was taught, to check.
            session (sqlalchemy.orm.session.Session): Session to connect to the db.

        Returns:
            bool: Whether the subject entry already exists in the db.
        """
        return (
            session.query(Subject)
            .filter(Subject.name == subject, Subject.natural_year == year)
            .count()
            != 0
        )

    @staticmethod
    def _student_subject_on_db(
        name: str,
        last_name: str,
        subject: str,
        year: str,
        mark: float,
        session: sqlalchemy.orm.session.Session,
    ) -> bool:
        """Check if the pairing student-subject already exists in the db.

        Args:
            name (str): Name of the student to check.
            last_name (str): Last name of the student to check.
            subject (str): Name of the subject to check.
            year (str): Year when the student took the subject, to check.
            mark (float): Mark the student has on the subject, to check.
            session (sqlalchemy.orm.session.Session): Session to connect to the db.

        Returns:
            bool: Whether the pairing student-subject already exists in db.
        """
        return (
            session.query(Student)
            .join(StudentSubject, Student.id == StudentSubject.student_id)
            .join(Subject, StudentSubject.subject_id == Subject.id)
            .filter(
                Student.name == name,
                Student.last_name == last_name,
                Subject.name == subject,
                Subject.natural_year == year,
                StudentSubject.mark == mark,
            )
            .count()
            == 0
        )

    def store_data_in_db(
        self, name: str, last_name: str, subject: str, year: str, mark: float,
    ) -> None:
        """Store the data in the db after checking that it does not already exist.

        Args:
            name (str): Name of the student to add to the db.
            last_name (str): Last name of the student to add to the db.
            subject (str): Name of the subject to add to the db.
            year (str): Year when the student took the subject to add to the db.
            mark (float): Mark the student got on the subject to add to the db.
        """
        with session_scope(
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            db_name=self._db_name,
        ) as session:
            new_student = self._get_or_create_student(
                name=name, last_name=last_name, session=session
            )
            student_subject = StudentSubject(mark=mark)
            student_subject.subject = self._get_or_create_subject(
                subject=subject, year=year, session=session
            )
            if not self._student_subject_on_db(
                name=name,
                last_name=last_name,
                subject=subject,
                year=year,
                mark=mark,
                session=session,
            ):
                new_student.subjects.append(student_subject)

    def get_number_passed_by_subject_and_year(
        self, subject: str, year: str
    ) -> int:
        """Get number of students that got a mark equal or greater than 5 on a given subject on a given year.

        Args:
            subject (str): Name of the subject to consult.
            year (str): Year the subject was taught to consult.

        Returns:
            int: Number of students that passed the subject in the given year as an answer for the query.
        """
        with session_scope(
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            db_name=self._db_name,
        ) as session:
            return (
                session.query(Student)
                .join(StudentSubject, Student.id == StudentSubject.student_id)
                .join(Subject, StudentSubject.subject_id == Subject.id)
                .filter(
                    Subject.name == subject,
                    Subject.natural_year == year,
                    StudentSubject.mark >= 5,
                )
                .count()
            )

    def get_number_failed_by_subject_and_year(
        self, subject: str, year: str
    ) -> int:
        """Get number of students that got a mark less than 5 on a given subject on a given year.

        Args:
            subject (str): Name of the subject to consult.
            year (str): Year the subject was taught to consult.

        Returns:
            int: Number of students that failed the subject in the given year as an answer for the query.
        """
        with session_scope(
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            db_name=self._db_name,
        ) as session:
            return (
                session.query(Student)
                .join(StudentSubject, Student.id == StudentSubject.student_id)
                .join(Subject, StudentSubject.subject_id == Subject.id)
                .filter(
                    Subject.name == subject,
                    Subject.natural_year == year,
                    StudentSubject.mark < 5,
                )
                .count()
            )

    def get_list_passed_by_subject_and_year(
        self, subject: str, year: str
    ) -> List[str]:
        """Get list of students that got a mark equal or greater than 5 on a given subject on a given year.

        Args:
            subject (str): Name of the subject to consult.
            year (str): Year the subject was taught to consult.

        Returns:
            List[str]: List of names and last names of students that passed the subject in the given year as an answer for the query.
        """
        with session_scope(
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            db_name=self._db_name,
        ) as session:
            students = []
            query = (
                session.query(Student.name, Student.last_name)
                .join(StudentSubject, Student.id == StudentSubject.student_id)
                .join(Subject, StudentSubject.subject_id == Subject.id)
                .filter(
                    Subject.name == subject,
                    Subject.natural_year == year,
                    StudentSubject.mark >= 5,
                )
                .all()
            )

            for element in query:
                students.append(" ".join(element))

        return students

    def get_list_failed_by_subject_and_year(
        self, subject: str, year: str
    ) -> List[str]:
        """Get list of students that got a mark less than 5 on a given subject on a given year.

        Args:
            subject (str): Name of the subject to consult.
            year (str): Year the subject was taught to consult.

        Returns:
            List[str]: List of names and last names of students that failed the subject in the given year as an answer for the query.
        """
        with session_scope(
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            db_name=self._db_name,
        ) as session:
            students = []
            query = (
                session.query(Student.name, Student.last_name)
                .join(StudentSubject, Student.id == StudentSubject.student_id)
                .join(Subject, StudentSubject.subject_id == Subject.id)
                .filter(
                    Subject.name == subject,
                    Subject.natural_year == year,
                    StudentSubject.mark < 5,
                )
                .all()
            )

            for element in query:
                students.append(" ".join(element))

        return students

    def get_list_students_by_subject_and_year(
        self, subject: str, year: str
    ) -> List[str]:
        """Get list of students that were enrolled on a given subject on a given year.

        Args:
            subject (str): Name of the subject to consult.
            year (str): Year the subject was taught to consult.

        Returns:
            List[str]: List of names and last names of students that were enrolled on the subject in the given year as an answer for the query.
        """
        with session_scope(
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            db_name=self._db_name,
        ) as session:
            students = []
            query = (
                session.query(Student.name, Student.last_name)
                .join(StudentSubject, Student.id == StudentSubject.student_id)
                .join(Subject, StudentSubject.subject_id == Subject.id)
                .filter(Subject.name == subject, Subject.natural_year == year,)
                .all()
            )

            for element in query:
                students.append(" ".join(element))

        return students

    def get_number_students_by_subject_and_year(
        self, subject: str, year: str
    ) -> int:
        """Get the number of students that were enrolled on a subject in a given year.

        Args:
            subject (str): Name of the subject to consult.
            year (str): Year the subject was taught to consult.

        Returns:
            int: Response from the query on how many students were enrolled in the subject in the given year.
        """
        with session_scope(
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            db_name=self._db_name,
        ) as session:
            return (
                session.query(Student)
                .join(StudentSubject, Student.id == StudentSubject.student_id)
                .join(Subject, StudentSubject.subject_id == Subject.id)
                .filter(Subject.name == subject, Subject.natural_year == year,)
                .count()
            )

    def get_list_subjects_by_year(self, year: str) -> List[str]:
        """Get the list of subjects taught in a given year.

        Args:
            year (str): Year to obtain the data from.

        Returns:
            List[str]: Response from the query to the db with the subjects that have an entrance with that year.
        """
        with session_scope(
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            db_name=self._db_name,
        ) as session:
            subjects = []
            query = (
                session.query(Subject.name)
                .filter(Subject.natural_year == year)
                .all()
            )

            for element in query:
                subjects.append(" ".join(element))

        return subjects
