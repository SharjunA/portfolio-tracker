from contextlib import contextmanager
from dotenv import load_dotenv

import os
import psycopg2

load_dotenv()


def create_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


@contextmanager
def get_connection():
    conn = create_connection()

    try:
        yield conn
    finally:
        conn.close()