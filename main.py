from src.data_handlers.route_data_manager import RouteDataManager
from src.data_handlers.weather_data_manager import WeatherDataManager
from src.ui.user_interface import UserInterface
from src.recommenders.route_recomender import RouteRecommender

def main():

    trails = RouteDataManager.load_routes("data/routes/routes.csv")
    weather_data = WeatherDataManager.fetch_weather_data(trails) 


    print(f"Loaded {len(trails)} trails")
    print("First 3 trails:", [t.name for t in trails[:3]])

    print(f"Fetched {len(weather_data)} weather entries")
    for w in weather_data[:3]:
        print(" ", w.date, "avg_temp:", w.avg_temp, "rain:", w.precipitation)

    user_prefs = UserInterface.user_run()

    recommender = RouteRecommender()
    pairs = recommender.recommend(trails, weather_data, user_prefs)

    UserInterface.print_routes(pairs)

main()