from datetime import date
from src.models.route import Route
from src.models.weather_data import WeatherData


class UserPreference():
    '''
    
    '''
    def __init__(self, *,
                    id: int = None,
                    user_name: str = 'default',
                    preferred_temp_min: float = 10.0,
                    preferred_temp_max: float = 30.0,
                    max_precipitation: float = 10.0,
                    max_difficulty: int = 3,
                    max_length_km: float = 20.0,
                    forecast_date: str = date.today()):
        self._id = id 
        self._name = user_name
        self._preferred_temp_min = preferred_temp_min
        self._preferred_temp_max = preferred_temp_max
        self._max_rain = max_precipitation
        self._max_difficulty = max_difficulty
        self._max_length_km = max_length_km
        self._forecast_date = forecast_date

    def __repr__(self):
        return (f"Name = {self._name}, \n"
                f"preferred_temp_min = {self._preferred_temp_min}, \n"
                f"preferred_temp_max = {self._preferred_temp_max}, \n"
                f"max_rain = {self._max_rain}, \n"
                f"max_difficulty = {self._max_difficulty}, \n"
                f"max_length_km = {self._max_length_km}, \n"
                f"forecast_date = {self._forecast_date})\n")

    def matches_route(self, route:Route) -> bool:
        '''
        Returns True if route difficulty and length are within user limits.
        '''
        return (route.difficulty <= self._max_difficulty and
                route.length_km <= self._max_length_km)

    def matches_weather(self, weather:WeatherData) -> bool:
        '''
        Returns True if average temperature and total rain are acceptable.
        '''
        temp_ok = self.preferred_temp_min <= weather.avg_temp <= self._preferred_temp_max
        rain_ok = (weather.precipitation <= self._max_rain)
        return temp_ok and rain_ok

    def update_preferences(self, 
                           preferred_temp=None,
                           max_rain=None, max_difficulty=None,
                           max_length=None):
        '''
        Update of preferences in place.
        '''
        if preferred_temp is not None:
            self._preferred_temp = preferred_temp
        if max_rain is not None:
            self._max_rain = max_rain
        if max_difficulty is not None:
            self._max_difficulty = max_difficulty
        if max_length is not None:
            self._max_length = max_length

    @property
    def id(self) -> int:
        return self._id
    @id.setter
    def id(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("User ID must be a non-negative integer")
        self._id = value
    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("User name must be a non-empty string")
        self._name = value.strip()   
    @property
    def preferred_temp_min(self) -> float:
        return self._preferred_temp_min
    @property
    def preferred_temp_max(self) -> float:
        return self._preferred_temp_max
    @property
    def max_precipitation(self) -> float:
        return self._max_rain
    @property
    def max_difficulty(self) -> int:
        return self._max_difficulty
    @property
    def max_length(self) -> float:
        return self._max_length
    @property
    def forecast_date(self) -> str:
        return self._forecast_date