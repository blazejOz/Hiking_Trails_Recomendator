from src.models.user_preference import UserPreference
from src.database.database_manager import DatabaseManager

class UserRepository:
    """
    Repository for managing user preferences in the database.
    """

    @staticmethod
    def add_user_preference(user_preference: UserPreference):
        """
        Add or update user preferences in the database.
        """
        conn = DatabaseManager.connect()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO user_preferences (user_name, preferred_temp_min, preferred_temp_max, max_precipitation, max_difficulty, max_length_km, preferred_terrain_types)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_preference._name, user_preference._preferred_temp_min,
             user_preference._preferred_temp_max, user_preference._max_rain,
             user_preference._max_difficulty, user_preference._max_length_km,
             user_preference._preferred_terrain_types)
        )
        
        conn.commit()
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
                user_name=row[0],
                preferred_temp_min=row[1],
                preferred_temp_max=row[2],
                max_precipitation=row[3],
                max_difficulty=row[4],
                max_length_km=row[5],
                preferred_terrain_types=row[6]
            )
        else:
            return None
        
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