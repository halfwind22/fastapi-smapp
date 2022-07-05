from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import config
import os

DATABASE_SERVER_HOST_NAME = os.getenv("DATABASE_SERVER_HOST_NAME")
DATABASE_SERVER_USERNAME = os.getenv("DATABASE_SERVER_USERNAME")
DATABASE_SERVER_PASSWORD = os.getenv("DATABASE_SERVER_PASSWORD")
DATABASE_SERVER_PORT = os.getenv("DATABASE_SERVER_PORT")
DATABASE_SERVER_SCHEMA = os.getenv("DATABASE_SERVER_SCHEMA")

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DATABASE_SERVER_USERNAME}:{DATABASE_SERVER_PASSWORD}@{DATABASE_SERVER_HOST_NAME}:{DATABASE_SERVER_PORT}/{DATABASE_SERVER_SCHEMA}"

#Create the SQLAlchemy engine

try:
    engine = create_engine(
    SQLALCHEMY_DATABASE_URL,pool_size=20, max_overflow=0)
except Exception as e:
    print("Connection Issues",e)

#Create a SessionLocal class
#Each instance of the SessionLocal class will be a database session.
# The instance of this class is a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()