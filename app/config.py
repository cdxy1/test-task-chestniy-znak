import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    _DB_HOST = os.getenv("DB_HOST")
    _DB_PORT = os.getenv("DB_PORT")
    _DB_USER = os.getenv("DB_USER")
    _DB_PASSWORD = os.getenv("DB_PASSWORD")
    _DB_NAME = os.getenv("DB_NAME")

    DB_DICT = {
        "dbname": _DB_NAME,
        "host": _DB_HOST,
        "user": _DB_USER,
        "password": _DB_PASSWORD,
        "port": _DB_PORT,
    }
