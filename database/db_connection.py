import mysql.connector
from mysql.connector import Error

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)


def get_connection():
    try:

        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if conn.is_connected():
            return conn

    except Error as e:

        print(f"Database Error : {e}")

        return None