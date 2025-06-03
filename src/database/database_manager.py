import sqlite3
import os
from src.models.route import Route

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

    @staticmethod
    def validate_route_data(route: Route):
        if not route.name or not isinstance(route.name, str):
            raise ValueError("Nazwa trasy jest wymagana.")
        if not route.region or not isinstance(route.region, str):
            raise ValueError("Region jest wymagany.")
        if route.length_km <= 0:
            raise ValueError("Długość trasy musi być większa od zera.")
        if route.difficulty not in [1, 2, 3]:
            raise ValueError("Trudność musi być 1, 2 lub 3.")
        if not (-90 <= route.start_lat <= 90) or not (-90 <= route.end_lat <= 90):
            raise ValueError("Szerokość geograficzna musi być w zakresie -90 do 90.")
        if not (-180 <= route.start_lon <= 180) or not (-180 <= route.end_lon <= 180):
            raise ValueError("Długość geograficzna musi być w zakresie -180 do 180.")
        