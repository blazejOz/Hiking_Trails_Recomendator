from src.data_handlers.route_data_manager import RouteDataManager
from src.data_handlers.weather_data_manager import WeatherDataManager

class TestWeatherDataManager():
    
    def run():

        routes = RouteDataManager.load_routes("data/routes/routes.csv")
        
        weathers = WeatherDataManager.fetch_weather_data(routes)

        
        