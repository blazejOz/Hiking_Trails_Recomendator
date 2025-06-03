import os
from src.data_handlers.route_data_manager import RouteDataManager
from src.database.repositories.route_repositories import RouteRepository


CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'legacy', 'routes.csv')

class MigrationTool:
    @staticmethod
    def migrate_routes():
        routes = RouteDataManager.load_routes(CSV_PATH)
        success_count = 0
        fail_count = 0
        if not routes:
            print("No routes found in the CSV file.")
            return
        print(f"Found {len(routes)} routes to migrate from CSV.")
        for route in routes:
            try:
                route_id = RouteRepository.add_route(route)
                print(f"Route '{route.name}' added with ID {route_id}.")
                success_count =+ 1
            except Exception as e:
                print(f"Error adding route '{route.name}': {e}")
                fail_count =+ 1
        print(f"Migration completed: {success_count} routes added successfully, {fail_count} failed.")

        
