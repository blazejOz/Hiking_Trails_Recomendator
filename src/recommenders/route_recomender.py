from src.models.route import Route
from src.models.weather_data import WeatherData
from src.models.user_preference import UserPreference

class RouteRecommender():
    def recommend(routes, weathers, prefs):
        good = []
        for r, w in zip(routes, weathers):
            if prefs.matches_route(r) and prefs.matches_weather(w):
                good.append((r, w))

        return good
