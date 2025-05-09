from src.data_handlers.route_data_manager import RouteDataManager
from src.data_handlers.weather_data_manager import WeatherDataManager

class TestWeatherDataManager():
    
    def run():

        routes = RouteDataManager.load_routes("data/routes/routes.csv")
        
        date = "2025-05-11"
        weathers = WeatherDataManager.fetch_weather_data(routes, date)
        print(f"Fetched weather for {len(weathers)} trails on {date}")

        print("\nFirst 3 weather summaries:")
        for w in weathers[:3]:
            print(
                f"{w.date} – avg_temp: {w.avg_temp}°C, "
                f"rain: {w.precipitation}mm, "
                f"cloud: {w.cloud_cover}%, "
                f"sunshine: {w.sunshine_hours}h"
            )    

        print("\n30-day weather statistics for first route:")
        WeatherDataManager.weather_statistic(routes[0])



        