import sqlite3


DATABASE_NAME = "student.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL,
            address TEXT
        )
        """
    )

    connection.commit()
    connection.close()