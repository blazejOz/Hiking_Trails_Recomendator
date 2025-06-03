import os
from src.data_handlers.route_data_manager import RouteDataManager
from src.database.repositories.route_repositories import RouteRepository


CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'legacy', 'routes.csv')

class MigrationTool:
    @staticmethod
    def migrate_routes():
        routes = RouteDataManager.load_routes(CSV_PATH)
        
        
