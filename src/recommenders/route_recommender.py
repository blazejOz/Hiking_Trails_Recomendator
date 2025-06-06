from typing import List
from src.models.route import Route
from src.models.weather_data import WeatherData
from src.models.user_preference import UserPreference
from src.database.repositories.route_repository import RouteRepository
from src.data_handlers.weather_data_manager import WeatherDataManager
from src.database.repositories.weather_repository import WeatherRepository


class RouteRecommender:

    def recommend(user:UserPreference) -> List[tuple[Route, WeatherData]]:
        """ Recommends routes based on user preferences"""
        routes = RouteRepository.get_all_routes()
        weather_data = []
        for route in routes:
            if WeatherRepository.check_weather_data_exists(user.forecast_date, route.id):
                weather = WeatherRepository.get_weather_data_by_route(user.forecast_date, route.id)
                weather_data.append(weather)
            else:
                weather = WeatherDataManager.fetch_date_forecast(route.id, user.forecast_date)
                WeatherRepository.add_weather_data(weather)
                weather_data.append(weather)
        
        recommended_routes = []
        for route, weather in zip(routes, weather_data):
            if user.matches_route(route) and user.matches_weather(weather):
                recommended_routes.append((route, weather))

        return recommended_routes
