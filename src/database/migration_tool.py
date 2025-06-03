import os
from src.data_handlers.route_data_manager import RouteDataManager
from src.database.repositories.route_repositories import RouteRepository


CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'legacy', 'routes.csv')

class MigrationTool:
    @staticmethod
    def migrate_routes():
        routes = RouteDataManager.load_routes(CSV_PATH)
        for route in routes:
            route_id = RouteRepository.add_route(route)
            print(f"Route '{route.name}' added with ID {route_id}.")
        print("Route migration completed successfully.")

        
