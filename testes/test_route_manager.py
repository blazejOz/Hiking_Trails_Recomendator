#from src.models.route import Route
from src.data_handlers.route_data_manager import RouteDataManager

class TestRouteManager():
    
    def run():

        trails = RouteDataManager.load_routes("data/routes/routes.csv")
        
        print(f"Loaded {len(trails)} trails")
        print("First 3 trails:", [t.name for t in trails[:3]])
        
