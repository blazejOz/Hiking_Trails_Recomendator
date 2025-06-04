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
    
    @staticmethod
    def get_all_routes():
        """
        Retrieve all routes from the database.
        """
        conn = DatabaseManager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM routes")
        rows = cursor.fetchall()
        conn.close()
        
        routes = []
        for row in rows:
            route = Route(
                id=row[0],
                name=row[1],
                region=row[2],
                start_lat=row[3],
                start_lon=row[4],
                end_lat=row[5],
                end_lon=row[6],
                length_km=row[7],
                elevation_gain=row[8],
                difficulty=row[9],
                terrain_type=row[10],
                tags=row[11].split(',') if row[11] else []
            )
            routes.append(route)
        
        return routes
    
    @staticmethod
    def get_route_count() -> int:
        """
        Get the total number of routes in the database.
        """
        conn = DatabaseManager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM routes")
        count = cursor.fetchone()[0]
        conn.close()
        return count