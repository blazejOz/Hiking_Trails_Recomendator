from src.data_handlers.route_data_manager import RouteDataManager
from src.data_handlers.weather_data_manager import WeatherDataManager
from src.recommenders.route_recomender import RouteRecommender
from src.models.user_preference import UserPreference


class UserInterface():

    @staticmethod
    def run():
        #Loading Routes 
        routes = RouteDataManager.load_routes("data/routes/routes.csv")
        #Feathcing weather from routes
        weather_data = WeatherDataManager.fetch_weather_data(routes)

        print("=== Preferencje użytkownika ===")
        preferred_temp = float(input("Preferowana temperatura(+/- 5stopni): "))
        max_rain = float(input("max rain: "))
        preferred_difficulty = int(input("Maksymalny poziom trudności (1 = łatwy, 3 = trudny): "))
        preferred_length = float(input("Maksymalna długość trasy (km): "))

        user_prefs = UserPreference(preferred_temp, max_rain, preferred_difficulty, preferred_length)

        recommender = RouteRecommender()
        pairs = recommender.recommend(routes, weather_data, user_prefs)

        UserInterface.print_routes(pairs)

        
    @staticmethod
    def print_routes(route_weather_pairs):
        print("\n=== Lista rekomendowanych tras ===")
        for route, weather in route_weather_pairs:
            print(f"{route.id}. {route.name}  ({route.region})")
            print(f"    Długość: {route.length_km} km")
            print(f"    Trudność: {route.difficulty}/3")
            print(f"    Szacowany czas: {route.estimated_completion()} h")
            print(f"    Komfort pogodowy: {weather.comfort_index()}")
            print(f"    Tagi: {', '.join(route.tags)}\n")

    