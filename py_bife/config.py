import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    DEBUG = bool(os.environ.get("DEBUG", False))
    TESTING = bool(os.environ.get("TESTING", False))
    SERVER_NAME = os.environ.get("SERVER_NAME")
