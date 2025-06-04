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
            (weather_data.date.isoformat(), weather_data.location_lat, weather_data.location_lon,
             weather_data.avg_temp, weather_data.min_temp, weather_data.max_temp,
             weather_data.precipitation, weather_data.sunshine_hours, weather_data.cloud_cover,
             weather_data.route_id),
        )
        conn.commit()
        weather_data.id = cursor.lastrowid
        conn.close()
        return weather_data.id