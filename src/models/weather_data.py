# src/models/weather_data.py

from datetime import date

class WeatherData:
    def __init__(
        self,
        *,
        date_str,
        location_id,
        avg_temp,
        min_temp,
        max_temp,
        precipitation,
        sunshine_hours,
        cloud_cover
    ):
        # Date as a datetime.date
        self._date = date.fromisoformat(date_str)
        # Identifier for the location (e.g. "lat,lon" or location name/id)
        self._location_id = location_id
        
        # Temperatures
        self._avg_temp       = float(avg_temp)
        self._min_temp       = float(min_temp)
        self._max_temp       = float(max_temp)
        
        # Precipitation (mm)
        self._precipitation  = float(precipitation)
        
        # Sunshine (hours)
        self._sunshine_hours = float(sunshine_hours)
        
        # Cloud cover (%)
        self._cloud_cover    = float(cloud_cover)
