from typing import List
from src.models.user_preference import UserPreference
from src.database.database_manager import DatabaseManager

class UserRepository:
    """
    Repository for managing user preferences in the database.
    """

    @staticmethod
    def add_user_preference(user_preference: UserPreference):
        """
        Add user preferences in the database.
        """
        conn = DatabaseManager.connect()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO user_preferences (user_name, preferred_temp_min, preferred_temp_max, max_precipitation, max_difficulty, max_length_km)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_preference.name, user_preference._preferred_temp_min,
             user_preference._preferred_temp_max, user_preference._max_rain,
             user_preference._max_difficulty, user_preference._max_length_km,
             )
        )
        conn.commit()
        user_preference._id = cursor.lastrowid  # Set the ID after insertion
        conn.close()

    @staticmethod
    def get_user_preference(user_name: str) -> UserPreference:
        """
        Retrieve user preferences from the database.
        """
        conn = DatabaseManager.connect()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT * FROM user_preferences WHERE user_name = ?
            """,
            (user_name,)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return UserPreference(
                id=row[0],
                user_name=row[1],
                preferred_temp_min=row[2],
                preferred_temp_max=row[3],
                max_precipitation=row[4],
                max_difficulty=row[5],
                max_length_km=row[6]
            )
        else:
            return None

    @staticmethod
    def check_user_exists(user_name: str) -> bool:
        """
        Check if a user exists in the database.
        """
        conn = DatabaseManager.connect()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT COUNT(*) FROM user_preferences WHERE user_name = ?
            """,
            (user_name,)
        )
        
        exists = cursor.fetchone()[0] > 0
        conn.close()
        
        return exists

    @staticmethod
    def update_user_preference(user_preference: UserPreference):
        """
        Update existing user preferences in the database.
        """
        conn = DatabaseManager.connect()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE user_preferences
            SET preferred_temp_min = ?, preferred_temp_max = ?, max_precipitation = ?, max_difficulty = ?, max_length_km = ?,
            WHERE user_name = ?
            """,
            (user_preference._preferred_temp_min, user_preference._preferred_temp_max,
             user_preference._max_rain, user_preference._max_difficulty,
             user_preference._max_length_km,
             user_preference.name)
        )
        
        conn.commit()
        conn.close()

    @staticmethod
    def print_all_users():
        """
        Print names off all available users
        """
        conn = DatabaseManager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT user_name FROM user_preferences")
        rows = cursor.fetchall()

        for row in rows:
            print(row)
        
    @staticmethod
    def get_user_count() -> int:
        """
        Get the total number of users in the database.
        """
        conn = DatabaseManager.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM user_preferences")
        count = cursor.fetchone()[0]
        
        conn.close()
        return count