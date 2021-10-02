from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os, time


# def create_connection_string():
#     load_dotenv()
#     db_type = os.getenv("DATABASE_TYPE")
#     username = os.getenv("DATABASE_USERNAME")
#     password = os.getenv("DATABASE_PASSWORD")
#     host = os.getenv("DATABASE_HOST")
#     port = os.getenv("DATABASE_PORT")
#     name = os.getenv("DATABASE_NAME")
#
#     return "{0}://{1}:{2}@{3}/{4}".format(db_type, username, password, host, name)


def wait_for_db(db_uri):
    """checks if database connection is established"""

    _local_engine = create_engine(db_uri)

    _LocalSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=_local_engine
    )

    up = False
    while not up:
        try:
            # Try to create session to check if DB is awake
            db_session = _LocalSessionLocal()
            # try some basic query
            db_session.execute("SELECT 1")
            db_session.commit()
        except Exception as err:
            print(f"Connection error: {err}")
            up = False
        else:
            up = True

        time.sleep(2)


# SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@db:5432/postgres"
SQLALCHEMY_DATABASE_URI = "postgresql://networks_lab2_user:123456@localhost:5432/networks_lab2"

wait_for_db(SQLALCHEMY_DATABASE_URI)

engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()