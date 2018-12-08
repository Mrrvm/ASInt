import Building
import User

import pymongo

class appDB:

    def __init__(self):
        #self.buildings = {}
        #self.users = {}
        cluster_url = "mongodb://carlos:12345678q.@clusterasint-shard-00-00-nk7xs.gcp.mongodb.net:27017,clusterasint-shard-00-01-nk7xs.gcp.mongodb.net:27017,clusterasint-shard-00-02-nk7xs.gcp.mongodb.net:27017/test?ssl=true&replicaSet=ClusterASInt-shard-0&authSource=admin&retryWrites=true"
        client = pymongo.MongoClient(cluster_url)
        self.database = client["chatist"]
        self.users = self.database["users"]
        self.buildings = self.database["buildings"]

    def addBuilding(self, name, lat, long, b_id):
        #self.buildings[b_id] = Building.Building(name, lat, long, b_id)
        x = self.buildings.insert_one({"id": b_id, "name": name, "lat": lat, "long": long})

    def removeBuilding(self, b_id):
        #self.buildings.pop(b_id, None)
        # print(b_id)
        x = self.buildings.delete_one({"id": b_id})
        # print(x.deleted_count, " documents deleted.")
        # print(list(self.buildings.find({"id": b_id})))

    def showAllBuildings(self):
        #return list(self.buildings.values())
        return list(self.buildings.find({},{ "_id": 0}))

    def showBuilding(self, id):
        #return self.buildings[id]
        return list(self.buildings.find({"id": id},{ "_id": 0}))

    def addUser(self, u_id, lat, long, u_name, u_photo):
        #self.users[u_id] = User.User(u_id, lat, long)
        new_user = {"id": u_id, "lat": lat,"long": long, "name": u_name, "photo": u_photo}
        x = self.users.insert_one(new_user)

    def getUser(self, id):
        return list(self.users.find({"id": id}, {"_id": 0}))

    def defineLocation(self, id, lat, long):
        #mycol = self.database["users"]
        #myquery = {"id": id}
        #mydoc = mycol.find(myquery)
        # mycol.update({ id: "id" }, {$set: { "lat": lat, "long": long}})
        pass

    def showAllUsers(self):
        return list(self.users.find({},{ "_id": 0}))


    def getUsersKeys(self, id):
        return self.users.keys()