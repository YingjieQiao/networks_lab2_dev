from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URI = "postgresql://networks_lab2_user:123456@localhost:5432/networks_lab2"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
