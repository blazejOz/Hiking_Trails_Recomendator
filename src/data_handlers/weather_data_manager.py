from src.models.route import Route
from src.models.weather_data import WeatherData
import requests

class WeatherDataManager:


    @staticmethod
    def featch_weather_data(routes, start_date: str = "2025-05-10"):
        '''
        For each Route in `routes`, fetch weather for a single day
        (start_date) and return a list of WeatherData objects.
        
        '''
        weather = []
        for trail in routes:
            lat, lon = trail.midpoint()
            forecast = WeatherDataManager.fetch_day_forecast(lat,lon,start_date)
            weather.append(WeatherData(
                date_str        = forecast["date"],
                location_id     = trail.region,
                avg_temp        = forecast["avg_temp"],
                min_temp        = forecast["min_temp"],
                max_temp        = forecast["max_temp"],
                precipitation   = forecast["precipitation"],
                sunshine_hours  = forecast["sunshine_hours"],
                cloud_cover     = forecast["cloud_cover"],
            ))
        
        return weather



    @staticmethod
    def fetch_day_forecast(lat: float, lon: float, date) -> dict:
        """
        Fetches the next-24h hourly forecast for (lat, lon) and
        returns a single dict with keys:
          date, location_id, avg_temp, precipitation,
          cloud_cover, sunshine_hours
        """
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&hourly=temperature_2m,precipitation,cloud_cover,sunshine_duration"
            f"&start_date={date}&end_date={date}"
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

        return {
            "date":           hourly["time"][0].split("T")[0],
            "location_id":    f"{lat},{lon}",
            "avg_temp":       round(sum(temps) / len(temps), 1),
            "min_temp":       round(min(temps), 1),
            "max_temp":       round(max(temps), 1),
            "precipitation":  round(sum(precs), 1),
            "sunshine_hours": round(sum(suns)/3600, 1),
            "cloud_cover":    round(sum(clouds) / len(clouds), 1),
        }

    @staticmethod
    def load_weather_data(file_path):
        pass