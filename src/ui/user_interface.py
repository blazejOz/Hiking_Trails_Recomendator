from src.data_handlers.route_data_manager import RouteDataManager
from src.data_handlers.weather_data_manager import WeatherDataManager
from src.recommenders.route_recomender import RouteRecommender
from src.models.user_preference import UserPreference


class UserInterface():

    def user_interface():

        print("=== Preferencje użytkownika ===")
        preferred_temp = float(input("Preferowana temperatura(+/- 5stopni): "))
        max_rain = float(input("max rain: "))
        preferred_difficulty = int(input("Maksymalny poziom trudności (1 = łatwy, 3 = trudny): "))
        preferred_length = float(input("Maksymalna długość trasy (km): "))

        return UserPreference(preferred_temp, max_rain, preferred_difficulty, preferred_length)

        
    @staticmethod
    def print_routes(routes):
        print("\n=== Lista rekomendowanych tras ===")
        for route in routes:
            print(f"{route.id}. {route.name}  ({route.region})")
            print(f"   Długość: {route.length_km} km  |  Trudność: {route.difficulty}/3")
            # jeśli zaimplementowałeś estimated_completion:
            print(f"   Szacowany czas: {route.estimated_completion()} h")
            print(f"   Tagi: {', '.join(route.tags)}\n")

    