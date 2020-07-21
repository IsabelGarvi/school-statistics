from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

Base = declarative_base()


class StudentSubject(Base):
    __tablename__ = "student-subject"
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
    # student = relationship(
    #     'Student', back_populates='subjects', cascade='all, delete',
    # )


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
    year = Column(Integer)  # year in which the subject is taught (p.e. 1)
    # students = relationship(
    #     'StudentSubject', back_populates='student', cascade='all, delete',
    # )


@contextmanager
def session_scope(user, password, host, port, db_name):
    """Provide a transactional scope around a series of operations."""
    connection_url = f"mysql://{user}:{password}@{host}:{port}/{db_name}"
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
    def __init__(self, db_user, db_pass, db_host, db_port, db_name):
        self._user = db_user
        self._password = db_pass
        self._host = db_host
        self._port = db_port
        self._db_name = db_name

    def _get_or_create_student(
        self, name: str, last_name: str, session
    ) -> Student:
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
    def _student_on_db(name: str, last_name: str, session) -> bool:
        return (
            session.query(Student)
            .filter(Student.name == name, Student.last_name == last_name)
            .count()
            != 0
        )

    def store_data_in_db(
        self,
        name: str,
        last_name: str,
        subject: str,
        year: int,
        natural_year: str,
        mark: float,
    ) -> None:
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
            link = StudentSubject(mark=mark)
            link.subject = Subject(
                name=subject, year=year, natural_year=natural_year
            )
            new_student.subjects.append(link)

    def _append_subject(self, student, subject, session) -> None:
        pass

    def _append_mark(self, mark):
        pass

    def get_number_passed_by_subject_and_year(
        self, subject: str, year: int, natural_year: str
    ) -> int:
        with session_scope(
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            db_name=self._db_name,
        ) as session:
            return (
                session.query(Student.name)
                .filter(
                    Subject.name == subject,
                    Subject.year == year,
                    Subject.natural_year == natural_year,
                    Subject.id == StudentSubject.subject_id,
                    StudentSubject.mark >= 5,
                )
                .count()
            )

    def get_number_failed_by_subject_and_year(
        self, subject: str, year: int, natural_year: str
    ) -> int:
        with session_scope(
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            db_name=self._db_name,
        ) as session:
            return (
                session.query(Student.name)
                .filter(
                    Subject.name == subject,
                    Subject.year == year,
                    Subject.natural_year == natural_year,
                    Subject.id == StudentSubject.subject_id,
                    StudentSubject.mark < 5,
                )
                .count()
            )

    def get_list_students_by_subject_and_year(
        self, subject: str, year: int, natural_year: str
    ) -> List[str]:
        with session_scope(
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            db_name=self._db_name,
        ) as session:
            return (
                session.query(Student.name)
                .filter(
                    Subject.name == subject,
                    StudentSubject.subject_id == Subject.id,
                    Subject.year == year,
                    Subject.natural_year == natural_year,
                )
                .all()
            )

    def get_number_students_by_subject_and_year(
        self, subject: str, year: int, natural_year: str
    ) -> int:
        with session_scope(
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            db_name=self._db_name,
        ) as session:
            return (
                session.query(Student.name)
                .filter(
                    Subject.name == subject,
                    StudentSubject.subject_id == Subject.id,
                    Subject.year == year,
                    Subject.natural_year == natural_year,
                )
                .count()
            )

    def get_list_subjects_by_year(
        self, year: int, natural_year: str
    ) -> List[str]:
        with session_scope(
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            db_name=self._db_name,
        ) as session:
            return (
                session.query(Subject.name)
                .filter(
                    Subject.year == year, Subject.natural_year == natural_year
                )
                .all()
            )
