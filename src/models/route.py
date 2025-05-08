class Route:
    def __init__(self, *, id, name, region, 
                 start_lat, start_lon, end_lat, end_lon, 
                 length_km, elevation_gain,
                 difficulty, terrain_type, tags):
        self._id = int(id)
        self._name = name
        self._region = region
        self._start = (float(start_lat), float(start_lon))
        self._end   = (float(end_lat),   float(end_lon))
        self._length_km       = float(length_km)
        self._elevation_gain  = int(elevation_gain)
        self._difficulty      = int(difficulty)
        self._terrain_type    = terrain_type
        self._tags            = tags.split(",")
        
    



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
        lat = (self._start[0] + self._end[0]) / 2
        lon = (self._start[1] + self._end[1]) / 2
        return (lat, lon)
    

    @property
    def region(self):
        return self._region

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name


    @property
    def start(self):
        return self._start
    
    @property
    def end(self):
        return self._end

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