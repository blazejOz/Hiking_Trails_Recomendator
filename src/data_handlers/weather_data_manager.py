import requests

class WeatherDataManager:

    @staticmethod
    def fetch_today_forecast(lat: float, lon: float) -> dict:
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
            "&forecast_days=1"
            "&timezone=Europe%2FWarsaw"
        )
        resp = requests.get(url)
        resp.raise_for_status() #raise errors
        hourly = resp.json()["hourly"] #dictionary of hourly data

        #lists of hourly data:
        temps = hourly["temperature_2m"]
        precs = hourly["precipitation"]  
        clouds = hourly["cloud_cover"]      
        suns  = hourly["sunshine_duration"]

        return {
            "date":           hourly["time"][0].split("T")[0],
            "location_id":    f"{lat},{lon}",
            "avg_temp":       round(sum(temps) / len(temps), 1),
            "precipitation":  round(sum(precs), 1),
            "cloud_cover":    round(sum(clouds) / len(clouds), 1),
            "sunshine_hours": round(sum(suns), 1),
        }
