import csv
from typing import List
from src.models.route import Route

class RouteDataManager:
    
    @staticmethod
    def load_routes(file_path):
        '''
        imports trails from csv file(data/routes/routes.csv) and return list of Route instances
        '''
        trails = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                #calling Route generator
                trails.append(Route(
                    id=row["id"],
                    name=row["name"],
                    region=row["region"],
                    start_lat=row["start_lat"],
                    start_lon=row["start_lon"],
                    end_lat=row["end_lat"],
                    end_lon=row["end_lon"],
                    length_km=row["length_km"],
                    elevation_gain=row["elevation_gain"],
                    difficulty=row["difficulty"],
                    terrain_type=row["terrain_type"],
                    tags=row["tags"],
                ))
        return trails
    
    @staticmethod
    def filter_routes(routes: List[Route],
                        *,
                        max_length:float = None,
                        max_difficulty:int = None,
                        terrain_type:str = None
                      ) -> List[Route]:
        filtered = routes

        if max_length is not None:
            filtered = [r for r in filtered if r.length_km <= max_length]

        if max_difficulty is not None:
            filtered = [r for r in filtered if r.difficulty <= max_difficulty]

        if terrain_type is not None:
            filtered = [r for r in filtered if r.terrain_type == terrain_type]
        
        return filtered

    @staticmethod
    def save_routes(routes: List[Route], filename="./data/routes/saved_routres.csv"):
        '''
        save routes to data/routes/saved_routes.csv
        '''
        fieldnames = [
        "id", "name", "region",
        "start_lat", "start_lon",
        "end_lat",   "end_lon",
        "length_km", "elevation_gain",
        "difficulty","terrain_type",
        "tags"
        ]

        with open(filename, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for route in routes:
                row = {
                    "id": route.id,
                "name": route.name,
                "region": route.region,
                "start_lat": route.start_lat,
                "start_lon": route.start_lon,
                "end_lat": route.end_lat,
                "end_lon": route.end_lon,
                "length_km": route.length_km,
                "elevation_gain": route.elevation_gain,
                "difficulty": route.difficulty,
                "terrain_type": route.terrain_type,
                "tags": ",".join(route.tags)
                }
                writer.writerows(row)