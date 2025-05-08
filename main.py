from src.data_handlers.route_data_manager import RouteDataManager
from src.data_handlers.weather_data_manager import WeatherDataManager
from src.ui.user_interface import UserInterface
from src.recommenders.route_recomender import RouteRecommender

def main():

    trails = RouteDataManager.load_trails("data/routes/routes.csv")
    weather_data = WeatherDataManager.fetch_weather_data(trails) 

    user_prefs = UserInterface.user_interface()

    recommender = RouteRecommender()
    recomended_trails = recommender.recommend(trails, weather_data, user_prefs)

    UserInterface.print_routes(recomended_trails)

main()