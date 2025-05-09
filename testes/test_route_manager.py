#from src.models.route import Route
from src.data_handlers.route_data_manager import RouteDataManager


trails = RouteDataManager.load_routes("data/routes/routes.csv")
