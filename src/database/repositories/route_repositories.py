from src.models.route import Route
from src.database.database_manager import DatabaseManager


class RouteRepository:
    
    @staticmethod
    def add_route(route: Route):
        """
        Add a new route to the database.
        """
        conn = DatabaseManager.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO routes (name, region, start_lat, start_lon, end_lat, end_lon, length_km, elevation_gain, difficulty, terrain_type, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (route.name, route.region, route.start_lat, route.start_lon,
             route.end_lat, route.end_lon, route.length_km, route.elevation_gain,
             route.difficulty, route.terrain_type, ','.join(route.tags)),
        )
        conn.commit()
        route.id = cursor.lastrowid
        conn.close()
        return route.id
