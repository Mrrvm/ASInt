import Building
import User

class appDB:

    def __init__(self):
        self.buildings = {}
        self.users = {}

    def addBuilding(self, name, lat, long, b_id):
        self.buildings[b_id] = Building.Building(name, lat, long, b_id)

    def removeBuilding(self, b_id):
        self.buildings.pop(b_id, None)

    def showAllBuildings(self):
        return list(self.buildings.values())

    def showBuilding(self, id):
        return self.buildings[id]