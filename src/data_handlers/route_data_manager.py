from src.models.route import Route
import csv

class RouteDataManager:
    
    @staticmethod
    def load_trails(file_path):
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