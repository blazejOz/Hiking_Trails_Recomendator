from src.models.route import Route
from src.models.weather_data import WeatherData
from src.models.user_preference import UserPreference



class RouteRecommender():
    def recommend(self, routes, weathers, prefs):
        good = []
        for r, w in zip(routes, weathers):
            if prefs.matches_route(r) and prefs.matches_weather(w):
                good.append((r, w))

        # 2) Sort by their combined score (highest first)
        #    We’ll just overwrite good with a sorted list of (route,weather)
        good.sort(key=lambda pair: prefs.compatibility_score(pair[0], pair[1]), 
                  reverse=True)

        # 3) Return just the Route objects
        return [pair[0] for pair in good]
