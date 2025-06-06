from src.models.route import Route
from src.models.weather_data import WeatherData
import requests
from datetime import date


class WeatherDataManager:

    @staticmethod
    def fetch_date_forecast(route: Route, forecast_date: str = None) -> WeatherData:
        '''
        Fetches the next-24h hourly forecast for Route.midpoint(lat, lon)
        '''
        if forecast_date is None:
            forecast_date = date.today()

        lat, lon = route.midpoint()

        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&hourly=temperature_2m,precipitation,cloud_cover,sunshine_duration"
            f"&start_date={forecast_date}&end_date={forecast_date}"
            "&timezone=Europe%2FWarsaw"
        )
        resp = requests.get(url)
        resp.raise_for_status() #raise errors
        hourly = resp.json()["hourly"] #dictionary of hourly data

        #lists of hourly data:
        temps = hourly["temperature_2m"]
        precs = hourly["precipitation"]  
        suns  = hourly["sunshine_duration"]
        clouds = hourly["cloud_cover"]      

        weather = WeatherData (
            id=             None,  # ID will be set by the database
            date =          forecast_date,
            location_lat=   lat,
            location_lon=   lon,
            avg_temp=       round(sum(temps) / len(temps), 1),
            min_temp=       round(min(temps), 1),
            max_temp=       round(max(temps), 1),
            precipitation=  round(sum(precs), 1),
            sunshine_hours= round(sum(suns)/3600, 2),
            cloud_cover=    round(sum(clouds) / len(clouds), 1),
            route_id=       route.id
        )
        return weather

    @staticmethod
    def weather_statistic(route: Route):
        '''
        Prints:
          - route.id and route.name
          - average temperature over past 30 days
          - average daily precipitation over past 30 days
          - average cloud cover over past 30 days
        '''
        lat, lon = route.midpoint()

        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&daily=temperature_2m_mean,precipitation_sum,cloudcover_mean"
            "&past_days=30"
            "&timezone=Europe%2FWarsaw"
        )
        resp = requests.get(url)
        resp.raise_for_status()
        daily = resp.json()["daily"]

        temps  = daily["temperature_2m_mean"]   
        precs  = daily["precipitation_sum"]      
        clouds = daily["cloudcover_mean"]        

        avg_temp  = round(sum(temps)  / len(temps), 1)
        avg_prec  = round(sum(precs)  / len(precs), 1)
        avg_cloud = round(sum(clouds)/ len(clouds), 1)

        print(f"{route.id}. {route.name}")
        print(f"  Średnia temperatura (30 dni):      {avg_temp} °C")
        print(f"  Średnie opady (30 dni):            {avg_prec} mm")
        print(f"  Średnie zachmurzenie (30 dni):     {avg_cloud}%\n")
