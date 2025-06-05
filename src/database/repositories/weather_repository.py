from src.models.route import Route
from src.models.weather_data import WeatherData
from src.database.database_manager import DatabaseManager

class WeatherRepository:
    
    @staticmethod
    def add_weather_data(weather_data: WeatherData):
        """
        Add weather data to the database.
        """
        conn = DatabaseManager.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO weather_data (date, location_lat, location_lon, avg_temp, min_temp, max_temp,
                                      precipitation, sunshine_hours, cloud_cover, route_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (weather_data.date, weather_data.location_lat, weather_data.location_lon,
             weather_data.avg_temp, weather_data.min_temp, weather_data.max_temp,
             weather_data.precipitation, weather_data.sunshine_hours, weather_data.cloud_cover,
             weather_data.route_id),
        )
        conn.commit()
        weather_data.id = cursor.lastrowid
        conn.close()
        return weather_data.id
    
    @staticmethod
    def get_all_weather_data() -> list[WeatherData]:
        """
        Retrieve all weather data from the database.
        """
        conn = DatabaseManager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather_data")
        rows = cursor.fetchall()
        conn.close()
        
        weather_data_list = []
        for row in rows:
            weather_data_list.append(WeatherData(
                id=row[0],
                date=row[1],
                location_lat=row[2],
                location_lon=row[3],
                avg_temp=row[4],
                min_temp=row[5],
                max_temp=row[6],
                precipitation=row[7],
                sunshine_hours=row[8],
                cloud_cover=row[9],
                route_id=row[10]
            ))
        
        return weather_data_list
    
    @staticmethod
    def get_weather_data_by_route(route_id: int) -> list[WeatherData]:
        pass

    staticmethod
    def check_weather_data_exists(date: str, route:Route ) -> bool:
        """
        Check if weather data for a specific date and location already exists in the database.
        """
        conn = DatabaseManager.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM weather_data
            WHERE date = ? AND route_id = ?
            """,
            (date, route.id)
        )
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists

    @staticmethod
    def get_weather_data_count() -> int:
        """
        Get the count of weather data entries in the database.
        """
        conn = DatabaseManager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM weather_data")
        count = cursor.fetchone()[0]
        conn.close()
        return count