class Route:
    def __init__(self, *, id, name, region, start_lat, start_lon,
                 end_lat, end_lon, length_km, elevation_gain,
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
    






    @property
    def midpoint(self):
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