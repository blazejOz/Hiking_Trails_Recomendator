from src.data_handlers.route_data_manager import RouteDataManager
from src.data_handlers.weather_data_manager import WeatherDataManager


def main():

    trails = RouteDataManager.load_trails("data/routes/routes.csv")
    weather_data = WeatherDataManager.load_weather_data(trails) 
    

main()