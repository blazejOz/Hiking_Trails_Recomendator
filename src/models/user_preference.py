class UserPreference():
    '''
    
    '''
    def __init__(self, preferred_temp, max_rain, max_difficulty, max_length):
        self._preferred_temp = preferred_temp
        self._max_rain = max_rain
        self._max_difficulty = max_difficulty
        self._max_length = max_length


    def matches_route(self, route) -> bool:
        '''
        Returns True if route difficulty and length are within user limits.
        '''
        return (route.difficulty <= self._max_difficulty and
                route.length_km <= self._max_length)

    def matches_weather(self, weather) -> bool:
        '''
        Returns True if average temperature and total rain are acceptable.
        '''
        temp_ok = (self._preferred_temp[0] <= weather.avg_temp <= self._preferred_temp[1])
        rain_ok = (weather.precipitation <= self._max_rain)
        return temp_ok and rain_ok

    def update_preferences(self, 
                           preferred_temp=None,
                           max_rain=None, max_difficulty=None,
                           max_length=None):
        '''
        Update any subset of preferences in place.
        '''
        if preferred_temp is not None:
            self._preferred_temp = preferred_temp
        if max_rain is not None:
            self._max_rain = max_rain
        if max_difficulty is not None:
            self._max_difficulty = max_difficulty
        if max_length is not None:
            self._max_length = max_length