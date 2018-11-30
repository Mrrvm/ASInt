import Building


class appDB:

    def __init__(self):
        self.buildings = []
        pass

    def addBuilding(self, name, lat, long, b_id):
        index = len(self.buildings)
        self.buildings[index] = Building.Building(name, lat, long, b_id)
