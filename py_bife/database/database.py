from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from py_bife import my_config


engine = create_engine(my_config.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def migrate():
    if my_config.TESTING:
        if my_config.RECREATE_DB:
            print("Dropping the schema")
            Base.metadata.drop_all(bind=engine)
        print("Creating the schema")
        Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
