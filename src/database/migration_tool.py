import os
from typing import List
from src.data_handlers.route_data_manager import RouteDataManager
from src.database.repositories.route_repositories import RouteRepository
from src.data_handlers.weather_data_manager import WeatherDataManager
from src.database.repositories.weather_repositories import WeatherRepository
from src.models.route import Route


CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'legacy', 'routes.csv')

class MigrationTool:
    @staticmethod
    def migrate_routes()-> List[Route]:
        routes = RouteDataManager.load_routes(CSV_PATH)
        success_count = 0
        fail_count = 0
        if not routes:
            print("No routes found in the CSV file.")
            return
        print(f"Found {len(routes)} routes to migrate from CSV.")
        for route in routes:
            try:
                route_id = RouteRepository.add_route(route)
                print(f"Route '{route.name}' added with ID {route_id}.")
                success_count =+ 1
            except Exception as e:
                print(f"Error adding route '{route.name}': {e}")
                fail_count =+ 1
        print(f"Migration completed: {success_count} routes added successfully, {fail_count} failed.")
        return routes
        
    @staticmethod
    def migrate_weather_data(routes: List[Route]):
        if not routes:
            print("No routes provided for weather data migration.")
            return
        for route in routes:
            try:
                weather_data = WeatherDataManager.fetch_day_forecast(route)
                weather_id = WeatherRepository.add_weather_data(weather_data)
                print(f"Weather data for route '{route.name}' added with ID {weather_id}.")
                print(f"Weather data for route '{route.name}' updated successfully.")
            except Exception as e:
                print(f"Error updating weather data for route '{route.name}': {e}")