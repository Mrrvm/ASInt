import pymongo
from bson.son import SON

building_range = 100.00

class appDB:

    def __init__(self):
        cluster_url = "mongodb://carlos:12345678q.@clusterasint-shard-00-00-nk7xs.gcp.mongodb.net:27017,clusterasint-shard-00-01-nk7xs.gcp.mongodb.net:27017,clusterasint-shard-00-02-nk7xs.gcp.mongodb.net:27017/test?ssl=true&replicaSet=ClusterASInt-shard-0&authSource=admin&retryWrites=true"
        client = pymongo.MongoClient(cluster_url)
        self.database = client["chatist"]
        self.users = self.database["users"]
        self.buildings = self.database["buildings"]
        self.buildings.create_index([("location", pymongo.GEOSPHERE)])
        self.users.create_index([("location", pymongo.GEOSPHERE)])


    def addBuilding(self, name, lat, long, b_id):
        self.buildings.insert_one({"id": b_id, "name": name, "location": {"type": "Point", "coordinates": [float(long), float(lat)]}})

    def removeBuilding(self, b_id):
        self.buildings.delete_one({"id": b_id})

    def showAllBuildings(self):
        return list(self.buildings.find({},{ "_id": 0, "location": 0}))

    def showBuilding(self, id):
        b_data = list(self.buildings.find({"id": id},{ "_id": 0}))[0]
        b_data['latitude'] = b_data['location']['coordinates'][1]
        b_data['longitude'] = b_data['location']['coordinates'][0]
        b_data.pop('location', None)
        return b_data

    def insideBuilding(self, u_id):
        user_location = list(self.users.find({"id": u_id}, {"location": 1, "range": 1}))[0]
        u_lat = user_location['location']['coordinates'][1]
        u_long = user_location['location']['coordinates'][0]
        query = {'location': {
            '$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates', [float(u_long), float(u_lat)])])),
                          ('$maxDistance', float(building_range))])}}
        #return without location as it's likely unnecessary
        return list(self.buildings.find(query,{ "_id": 0, "location": 0}))

    def showAllUsers(self):
        return list(self.users.find({},{ "_id": 0, "photo": 0, "location": 0, "range": 0}))

    def showUser(self, id):
        user_data = list(self.users.find({"id": id}, {"_id": 0, "photo": 0}))[0]
        user_data['latitude'] = user_data['location']['coordinates'][1]
        user_data['longitude'] = user_data['location']['coordinates'][0]
        user_data.pop('location', None)
        return user_data

    def addUser(self, u_id, u_lat, u_long, u_range, u_name, u_photo):
        if not list(self.users.find({"id": u_id})):
            new_user = {"id": u_id, "name": u_name, "photo": u_photo, "range": u_range, "location": {"type": "Point", "coordinates": [float(u_long), float(u_lat)]}}
            self.users.insert_one(new_user)

    def getUser(self, u_id):
        return list(self.users.find({"id": u_id}, {"_id": 0}))

    def defineLocation(self, u_id, u_lat, u_long):
        self.users.update_many({"id": u_id}, {"$set": {"location": {"type": "Point", "coordinates": [float(u_long), float(u_lat)]}}})

    def defineRange(self, u_id, u_range):
        self.users.update_many({"id": u_id}, {"$set": {"range": u_range}})

    def nearbyUsers(self, u_id):
        user_location = list(self.users.find({"id": u_id}, {"location": 1, "range": 1}))[0]
        u_lat = user_location['location']['coordinates'][1]
        u_long = user_location['location']['coordinates'][0]
        u_range = user_location['range']
        query = {'location': {'$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates',
                                        [float(u_long), float(u_lat)])])),
                                       ('$maxDistance', float(u_range))])}, 'id': {'$ne': u_id}}
        # return without location as it's likely unnecessary
        return list(self.users.find(query, {"_id": 0, "location": 0, "range": 0}))

    #, 'id': {'$not': u_id}