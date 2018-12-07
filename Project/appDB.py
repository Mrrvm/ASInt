import Building
import User

import pymongo

class appDB:

    def __init__(self):
        self.buildings = {}
        self.users = {}
        cluster_url = "mongodb://carlos:12345678q.@clusterasint-shard-00-00-nk7xs.gcp.mongodb.net:27017,clusterasint-shard-00-01-nk7xs.gcp.mongodb.net:27017,clusterasint-shard-00-02-nk7xs.gcp.mongodb.net:27017/test?ssl=true&replicaSet=ClusterASInt-shard-0&authSource=admin&retryWrites=true"
        client = pymongo.MongoClient(cluster_url)
        self.database = client["chatist"]

    def addBuilding(self, name, lat, long, b_id):
        self.buildings[b_id] = Building.Building(name, lat, long, b_id)

    def removeBuilding(self, b_id):
        self.buildings.pop(b_id, None)

    def showAllBuildings(self):
        return list(self.buildings.values())

    def showBuilding(self, id):
        return self.buildings[id]

    def addUser(self, u_id, lat, long):
        self.users[u_id] = User.User(u_id, lat, long)
        mycol = self.database["users"]
        mydict = {"id": u_id, "lat": lat,"long": long}
        x = mycol.insert_one(mydict)

    def showAllUsers(self):
        return list(self.users.values())

    def showUser(self, id):
        return self.users[id]

    def getUsersKeys(self, id):
        return self.users.keys()