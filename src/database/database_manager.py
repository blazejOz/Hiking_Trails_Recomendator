import sqlite3
import os
from src.models.route import Route
from src.models.weather_data import WeatherData

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
        if not isinstance(route, Route):
            raise TypeError("Expected a Route instance")
        if not route._name or not isinstance(route._name, str):
            raise ValueError("Route name must be a non-empty string")
        if not isinstance(route._region, str):
            raise ValueError("Region must be a string")
        if not (-90 <= route._start_lat <= 90) or not (-180 <= route._start_lon <= 180):
            raise ValueError("Start coordinates must be valid latitude and longitude")
        if not (-90 <= route._end_lat <= 90) or not (-180 <= route._end_lon <= 180):
            raise ValueError("End coordinates must be valid latitude and longitude")
        if route._length_km <= 0:
            raise ValueError("Length must be a positive number")
        if route._elevation_gain < 0:
            raise ValueError("Elevation gain cannot be negative")
        if route._difficulty not in [1, 2, 3, 4, 5]:
            raise ValueError("Difficulty must be 1, 2, 3, 4, or 5")
        if route._terrain_type not in ["mountain", "forest", "urban", "lakeside"]:
            raise ValueError("Invalid terrain type")
        if not isinstance(route._tags, list) or any(not isinstance(tag, str) for tag in route._tags):
            raise ValueError("Tags must be a list of strings")

    @staticmethod
    def validate_weather_data(weather: WeatherData):
        if not isinstance(weather, WeatherData):
            raise TypeError("Expected a WeatherData instance")
        if not isinstance(weather._date, str) or not weather._date:
            raise ValueError("Date must be a non-empty string")
        if not isinstance(weather._location_lat, (int, float)):
            raise ValueError("Location latitude must be a number")
        if not isinstance(weather._location_lon, (int, float)):
            raise ValueError("Location longitude must be a number")
       
       