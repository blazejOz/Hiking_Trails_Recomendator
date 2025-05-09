from src.data_handlers.route_data_manager import RouteDataManager

class TestRouteManager():
    
    def run():

        routes = RouteDataManager.load_routes("data/routes/routes.csv")
        
        print(f"Loaded {len(routes)} trails")
        print("First 3 trails:", [t.name for t in routes[:3]])
        
        filtered = RouteDataManager.filter_routes(routes, max_length = 10)
        
        print(f"After filtering: {len(filtered)} trails remaining")

        RouteDataManager.save_routes(filtered)
    