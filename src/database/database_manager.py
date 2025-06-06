from datetime import datetime
import sqlite3
import os
from src.models.route import Route
from src.models.user_preference import UserPreference
from src.models.weather_data import WeatherData

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR,'..', '..', 'data', 'database', 'recommender.db')
SCHEMA_PATH = os.path.join(BASE_DIR, '..', '..', 'sql', 'schema.sql')
BACKUP_DIR = os.path.join(BASE_DIR,'..', '..', 'data', 'backups')

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
    def backup_database():
            """Create a backup of the database in BACKUPS_DIR with current date."""
            if not os.path.exists(DB_PATH):
                raise FileNotFoundError("Database does not exist.")
            
            os.makedirs(BACKUP_DIR, exist_ok=True)
            date_str = datetime.now().strftime("%Y%m%d")
            backup_filename = f"db_backup_{date_str}.sqlite3"
            backup_path = os.path.join(BACKUP_DIR, backup_filename)
            
            with open(backup_path, 'wb') as backup_file:
                with open(DB_PATH, 'rb') as db_file:
                    backup_file.write(db_file.read())
            
            return backup_path

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
    def validate_user_preference_data(user: UserPreference):
        if not isinstance(user, UserPreference):
            raise TypeError("Expected a UserPreference instance")
        if not isinstance(user._preferred_difficulty, int) or user._preferred_difficulty not in [1, 2, 3, 4, 5]:
            raise ValueError("Preferred difficulty must be an integer between 1 and 5")
        if not isinstance(user._max_length_km, (int, float)) or user._max_length_km <= 0:
            raise ValueError("Maximum length must be a positive number")
        if not isinstance(user.preferred_temp_min, (int, float)):
            raise ValueError("Preferred minimum temperature must be a number")
        if not isinstance(user.preferred_temp_max, (int, float)):
            raise ValueError("Preferred maximum temperature must be a number")
        
       