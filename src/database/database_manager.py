import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR,'..', '..', 'data', 'database', 'recommender.db')
SCHEMA_PATH = os.path.join(BASE_DIR, '..', '..', 'sql', 'schema.sql')

class DatabaseManager:

    @staticmethod
    def connect():
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    @staticmethod
    def initialize_database():
        """Create the database file and tables if they don't exist."""
        if os.path.exists(DB_PATH):
            return

        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = DatabaseManager.connect()
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()