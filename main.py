from src.ui.user_interface import UserInterface

#test
from tests.test_route_manager import TestRouteManager
from tests.test_weather_data_manager import TestWeatherDataManager

def main():
    print()
    #UserInterface.run()
    
    #tests:
    #TestRouteManager.run()

    TestWeatherDataManager.run()



main()