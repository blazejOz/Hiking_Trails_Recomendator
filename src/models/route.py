class Route:
    def __init__(self, *, id, name, region, 
                 start_lat, start_lon, end_lat, end_lon, 
                 length_km, elevation_gain,
                 difficulty, terrain_type, tags):
        
        if float(length_km) <= 0:
            raise ValueError("Długość trasy musi być dodatnia.")
        if int(elevation_gain) < 0:
            raise ValueError("Przewyższenie nie może być ujemne.")
        if not (1 <= int(difficulty) <= 5):
            raise ValueError("Trudność musi być w zakresie 1-5.")
        if not (-90 <= float(start_lat) <= 90) or not (-90 <= float(end_lat) <= 90):
            raise ValueError("Szerokość geograficzna musi być w zakresie -90 do 90.")
        if not (-180 <= float(start_lon) <= 180) or not (-180 <= float(end_lon) <= 180):
            raise ValueError("Długość geograficzna musi być w zakresie -180 do 180.")
        valid_terrain = {"forest", "mountain", "urban", "lakeside"}
        if terrain_type not in valid_terrain:
            raise ValueError(f"Typ terenu musi być jednym z: {valid_terrain}")

        self._id = int(id) if id is not None else None
        self._name = name
        self._region = region
        self._start_lat = float(start_lat)
        self._start_lon = float(start_lon)
        self._end_lat   = float(end_lat)
        self._end_lon   = float(end_lon)
        self._length_km       = float(length_km)
        self._elevation_gain  = int(elevation_gain)
        self._difficulty      = int(difficulty)
        self._terrain_type    = terrain_type
        if isinstance(tags, str):
            self._tags = tags.split(",")
        elif isinstance(tags, list):
            self._tags = tags
        else:
            self._tags = []
        
    



    def check_preference(self, prefs) -> bool:
        '''
        Returns True if this route's length and difficulty
        are within the user's preferences.
        '''
        return prefs.matches_route(self)

    def estimated_completion(self) -> float:
        '''
        Estimates completion time in hours, based on:
          - base speeds by terrain
          - difficulty multiplier
          - +1h per 600m elevation gain
        '''
        # base walking speeds (km/h) by terrain
        base_speeds = {
            "mountain": 3.5,
            "forest":   4.0,
            "urban":    5.0,
            "lakeside": 4.5
        }
        speed = base_speeds.get(self._terrain_type, 4.0)

        # difficulty multiplier: 1→1.0, 2→1.3, 3→1.6
        diff_mult = {1:1.0, 2:1.3, 3:1.6}.get(self._difficulty, 1.0)

        moving_time = (self._length_km / speed) * diff_mult
        climb_time  = self._elevation_gain / 600.0
        total_hours = moving_time + climb_time
        
        return round(total_hours, 2)

    def midpoint(self) -> tuple:
        lat = (self._start_lat + self._end_lat) / 2
        lon = (self._start_lon + self._end_lat) / 2
        return (lat, lon)
    

    @property
    def region(self):
        return self._region

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = int(value)

    @property
    def name(self):
        return self._name


    @property
    def start_lat(self):
        return self._start_lat
    
    @property
    def start_lon(self):
        return self._start_lon

    @property
    def end_lat(self):
        return self._end_lat

    @property
    def end_lon(self):
        return self._end_lon

    @property
    def length_km(self):
        return self._length_km

    @property
    def elevation_gain(self):
        return self._elevation_gain

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def terrain_type(self):
        return self._terrain_type

    @property
    def tags(self):
        return self._tags
    
    