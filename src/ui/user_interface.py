from src.data_handlers.route_data_manager import RouteDataManager
from src.data_handlers.weather_data_manager import WeatherDataManager
from src.models.user_preference import UserPreference
from src.recommenders.route_recomender import RouteRecommender


class UserInterface():

    def user_interface():

        print("=== Preferencje użytkownika ===")
        preferred_temp = float(input("Preferowana temperatura: "))
        max_rain = float(input("max rain: "))
        preferred_length = float(input("Maksymalna długość trasy (km): "))
        preferred_difficulty = int(input("Maksymalny poziom trudności (1 = łatwy, 3 = trudny): "))

    