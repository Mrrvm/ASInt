class User:
    def __init__(self, id, lat, long, name, photo):
        self.id = id
        self.lat = lat
        self.long = long
        self.name = name
        self.photo = photo

    def __str__(self):
        return "%s - %f - %f" % (self.id, self.lat, self.long, self.name)

    #log = {"user": pode ser null, "building": pode ser null, "data": xpto}

