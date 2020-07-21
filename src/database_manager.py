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
    student = relationship(
        "Student", back_populates="subjects", cascade="all, delete",
    )
    subject = relationship(
        "Subject", back_populates="students", cascade="all, delete",
    )
    mark = Column(Float)


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String(50))
    last_name = Column(String(50))
    subjects = relationship(
        "StudentSubject", back_populates="subject", cascade="all, delete",
    )


class Subject(Base):
    __tablename__ = "subject"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String(50))
    students = relationship(
        "StudentSubject", back_populates="student", cascade="all, delete",
    )
    natural_year = relationship(
        "Years", back_populates="year", cascade="all, delete",
    )  # año natural en el que se cursa la asignatura
    year = Column(Integer)  # curso


class Years(Base):
    __tablename__ = "years"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    year = Column(Integer)
    subject = relationship(
        "Subject", back_populates="id", cascade="all, delete",
    )


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

    def store_data_in_db(self, *args, **kwargs):
        pass

    def get_number_passed_by_subject_and_year(self, subject, year):
        pass

    def get_number_failed_by_subject_and_year(self, subject, year):
        pass

    def get_list_students_by_subject_and_year(self, subject, year):
        pass

    def get_number_students_by_subject_and_year(self, subject, year):
        pass

    def get_list_subjects_by_year(self, year):
        pass
