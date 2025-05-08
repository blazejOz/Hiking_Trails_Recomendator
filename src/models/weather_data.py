# src/models/weather_data.py

from datetime import date

class WeatherData:
    def __init__(self, *, date_str, location_id, 
                avg_temp, min_temp,  max_temp,
                precipitation, sunshine_hours,cloud_cover ):

        self._date = date.fromisoformat(date_str)
        self._location_id = location_id
        self._avg_temp       = float(avg_temp)
        self._min_temp       = float(min_temp)
        self._max_temp       = float(max_temp)
        self._precipitation  = float(precipitation)
        self._sunshine_hours = float(sunshine_hours)
        self._cloud_cover    = float(cloud_cover)


    def is_sunny(self):
        return self._cloud_cover < 30

    def is_rainy(self):
        return self._precipitation > 0

    def comfort_index(self):
        return 100