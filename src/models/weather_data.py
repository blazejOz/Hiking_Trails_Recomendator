# src/models/weather_data.py

from datetime import date

class WeatherData:
    def __init__(self, *, date_str, location_id,
                 avg_temp, min_temp, max_temp,
                 precipitation, sunshine_hours, cloud_cover):
        self._date            = date.fromisoformat(date_str)
        self._location_id     = location_id
        self._avg_temp        = float(avg_temp)
        self._min_temp        = float(min_temp)
        self._max_temp        = float(max_temp)
        self._precipitation   = float(precipitation)
        self._sunshine_hours  = float(sunshine_hours)
        self._cloud_cover     = float(cloud_cover)

    def is_sunny(self):
        return self._cloud_cover < 30

    def is_rainy(self):
        return self._precipitation > 0

    def comfort_index(self):
        temp_score  = max(0, 100 - abs(self._avg_temp - 20) * 4)
        rain_score  = max(0, 100 - self._precipitation * 10)
        cloud_score = max(0, 100 - self._cloud_cover)
        return round((temp_score + rain_score + cloud_score) / 3)


    @property
    def date(self):
        return self._date

    @property
    def location_id(self):
        return self._location_id

    @property
    def avg_temp(self):
        return self._avg_temp

    @property
    def min_temp(self):
        return self._min_temp

    @property
    def max_temp(self):
        return self._max_temp

    @property
    def precipitation(self):
        return self._precipitation

    @property
    def sunshine_hours(self):
        return self._sunshine_hours

    @property
    def cloud_cover(self):
        return self._cloud_cover

    
