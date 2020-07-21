import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database_manager import SchoolDB


db_name = os.environ["DB_NAME"]
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_host = os.environ["DB_HOST"]
db_port = os.environ["DB_PORT"]

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
