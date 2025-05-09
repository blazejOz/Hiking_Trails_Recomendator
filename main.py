from src.data_handlers.route_data_manager import RouteDataManager
from src.data_handlers.weather_data_manager import WeatherDataManager
from src.ui.user_interface import UserInterface
from src.recommenders.route_recomender import RouteRecommender

#test
from tests.test_route_manager import TestRouteManager 

def main():
    print()
    #UserInterface.run()
    
    #tests:
    TestRouteManager.run()



main()