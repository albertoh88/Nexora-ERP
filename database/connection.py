import sqlite3
from contextlib import closing
from pathlib import Path

DATABASE_DIR = Path(__file__).resolve().parent
DB_PATH = DATABASE_DIR /  "nexora.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"


def initialize_database():
    with closing(sqlite3.connect(DB_PATH)) as connection:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)
        connection.commit()


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute('PRAGMA foreign_keys=ON')
    return connection