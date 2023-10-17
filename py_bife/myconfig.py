import os
import multiprocessing
from dotenv import load_dotenv

environment = os.environ.get("APP_ENVIRONMENT", "development")
if environment == "production":
    load_dotenv(".env.prod")
else:
    load_dotenv()

# Determine the number of CPU cores
recommended_number_workers = (multiprocessing.cpu_count() * 2) + 1


class MyConfig(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    TESTING = bool(os.environ.get("TESTING", "True") == "True")
    HOST = os.environ.get("HOST", "localhost")
    PORT = int(os.environ.get("PORT", "8080"))
    WORKERS = int(os.environ.get("WORKERS", recommended_number_workers))
    RECREATE_DB = bool(os.environ.get("RECREATE_DB", "True") == "True")

    def fix_workers(self):
        if self.WORKERS > recommended_number_workers:
            self.WORKERS = recommended_number_workers
