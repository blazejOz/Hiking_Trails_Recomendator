from src.data_handlers.route_data_manager import RouteDataManager
from src.data_handlers.weather_data_manager import WeatherDataManager


def main():

    trails = RouteDataManager.load_trails("data/routes/routes.csv")

    for r in trails[:3]:
        lat, lon = r.midpoint
        summary = WeatherDataManager.fetch_today_forecast(lat, lon)
        print(f"{r.name} - {summary}")



main()