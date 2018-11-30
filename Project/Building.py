class Building:
    def __init__(self, name, lat, long, b_id):
        self.name = name
        self.lat = lat
        self.long = long
        self.id = b_id

    def __str__(self):
        return "%d - %s - [%s - %s]" % (self.id, self.name, self.lat, self.long)

