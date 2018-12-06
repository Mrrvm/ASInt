class User:
    def __init__(self, id, lat, long):
        self.id = id
        self.lat = lat
        self.long = long

    def __str__(self):
        return "%s - %f - %f" % (self.id, self.lat, self.long)

