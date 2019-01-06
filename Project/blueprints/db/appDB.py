import pymongo
import uuid
import datetime
from bson.son import SON


building_range = 100.00

class appDB:


    def __init__(self):
        cluster_url = "mongodb://carlos:12345678q.@clusterasint-shard-00-00-nk7xs.gcp.mongodb.net:27017,clusterasint-shard-00-01-nk7xs.gcp.mongodb.net:27017,clusterasint-shard-00-02-nk7xs.gcp.mongodb.net:27017/test?ssl=true&replicaSet=ClusterASInt-shard-0&authSource=admin&retryWrites=true"
        client = pymongo.MongoClient(cluster_url)
        self.database = client["chatist"]
        self.users = self.database["users"]
        self.buildings = self.database["buildings"]
        self.movements = self.database["movements"]
        self.messages = self.database["messages"]
        self.message_table = self.database["message_table"]
        self.buildings.create_index([("location", pymongo.GEOSPHERE)])
        self.users.create_index([("location", pymongo.GEOSPHERE)])
        self.bots = self.database["bots"]
        self.movements = self.database["movements"]

        # get maximum id from existing messages
        messages_ids_results = list(self.message_table.find({}, {"_id": 0, "id": 1}))
        if not messages_ids_results:
            self.message_id = 0
        else:
            messages_ids = []
            for message in messages_ids_results:
                messages_ids.append(int(message["id"]))
            self.message_id = max(messages_ids)

        # get maximum id from existing bots
        bots_ids_results = list(self.bots.find({}, {"_id": 0, "id": 1}))
        if not bots_ids_results:
            self.bot_id = 0
        else:
            bots_ids = []
            for bot in bots_ids_results:
                bots_ids.append(int(bot["id"]))
            self.bot_id = max(bots_ids)


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

    def insideBuilding(self, b_id, excluding, u_id, option):
        building_location = list(self.buildings.find({"id": b_id}, {"location": 1}))[0]
        lat_ = building_location['location']['coordinates'][1]
        long_ = building_location['location']['coordinates'][0]
        query = {'location': {
            '$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates', [float(long_), float(lat_)])])),
                          ('$maxDistance', float(building_range))])}}
        # has to exclude sender of messages of searcher of nearby
        if excluding:
            query['id'] = {'$ne': u_id}
        if option is 'IDS':
            return list(self.users.find(query, {"_id": 0, "id": 1}))
        elif option is 'PHOTO':
            return list(self.users.find(query, {"_id": 0, "location": 0, "range": 0}))

    def containingBuildings(self, u_id):
        user_location = list(self.users.find({"id": u_id}, {"location": 1, "range": 1}))[0]
        u_lat = user_location['location']['coordinates'][1]
        u_long = user_location['location']['coordinates'][0]
        query = {'location': {
            '$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates', [float(u_long), float(u_lat)])])),
                          ('$maxDistance', float(building_range))])}}
        #return without location as it's likely unnecessary
        return list(self.buildings.find(query, {"_id": 0, "location": 0}))

    def showAllUsers(self):
        return list(self.users.find({"logged_in": "yes"},{ "_id": 0, "photo": 0, "location": 0, "range": 0}))

    def showUser(self, id):
        user_data = list(self.users.find({"id": id, "logged_in": "yes"}, {"_id": 0, "photo": 0}))[0]
        user_data['latitude'] = user_data['location']['coordinates'][1]
        user_data['longitude'] = user_data['location']['coordinates'][0]
        user_data.pop('location', None)
        return user_data

    def showAllBots(self):
        return list(self.bots.find({},{ "_id": 0}))

    def newBot(self, allowed_buildings):
        self.bot_id = self.bot_id + 1
        bot_key = str(uuid.uuid4())
        new_bot = {"id": self.bot_id, "key": bot_key, "buildings": allowed_buildings}
        self.bots.insert_one(new_bot)
        new_bot.pop('_id', None)
        return new_bot

    def deleteBot(self, bot_id):
        self.bots.delete_one({"id": int(bot_id)})


    def botKey(self, bot_id):
        query_result = list(self.bots.find({"id": bot_id},{"_id":0, "key": 1}))
        if not query_result:
            return None
        else:
            return query_result[0]['key']

    def botMessage(self, bot_id, message):
        building_list = list(self.bots.find({"id": bot_id}, {"_id": 0, "buildings": 1}))[0]['buildings']
        to_list = []
        for id in building_list:
            to_list.extend(self.insideBuilding(id, False, None, "IDS"))
        if not to_list:
            pass
        else:
            self.message_id = self.message_id + 1
            self.messages.insert_one({"message": message, "id": self.message_id, "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            for destination in to_list:
                message = {"from": "BOT " + str(bot_id), "to": destination["id"], "id": self.message_id, "rcv": 0}
                # if message was sent to entire building then saves building id in message
                message["buildings"] = building_list
                self.message_table.insert_one(message)
                self.message_table.insert_one({"from": "BOT " + str(bot_id), "to": destination["id"], "id": self.message_id, "rcv": 0})


    def showAllMovements(self):
        return list(self.movements.find({},{ "_id": 0}))

    def showUserMovements(self, u_id):
        return list(self.movements.find({"user_id": u_id},{ "_id": 0}))


    def addUser(self, u_id, u_lat, u_long, u_range, u_name, u_photo):
        if not list(self.users.find({"id": u_id})):
            new_user = {"id": u_id, "name": u_name, "photo": u_photo, "range": u_range, "location": {"type": "Point", "coordinates": [float(u_long), float(u_lat)]}, "logged_in": "yes"}
            self.users.insert_one(new_user)
        else:
            self.users.update_many({"id": u_id}, {"$set": {"logged_in": "yes"}})

    def logoutUser(self, u_id):
        if list(self.users.find({"id": u_id, "logged_in": "yes"})):
            self.users.update_many({"id": u_id}, {"$set": {"logged_in": "no"}})

    def getUser(self, u_id):
        return list(self.users.find({"id": u_id}, {"_id": 0}))

    def defineLocation(self, u_id, u_lat, u_long):
        self.users.update_many({"id": u_id}, {"$set": {"location": {"type": "Point", "coordinates": [float(u_long), float(u_lat)]}}})
        new_movement = {"user_id": u_id, "new_latitude": u_lat, "new_longitude": u_long, "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self.movements.insert_one(new_movement)

    def defineRange(self, u_id, u_range):
        self.users.update_many({"id": u_id}, {"$set": {"range": u_range}})

    def nearbyUsers(self, u_id, option):
        user_location = list(self.users.find({"id": u_id}, {"location": 1, "range": 1}))[0]
        u_lat = user_location['location']['coordinates'][1]
        u_long = user_location['location']['coordinates'][0]
        u_range = user_location['range']
        query = {'location': {'$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates',
                                        [float(u_long), float(u_lat)])])),
                                       ('$maxDistance', float(u_range))])}, 'id': {'$ne': u_id}}
        # return without location as it's likely unnecessary
        if option is 'IDS':
            return list(self.users.find(query, {"_id": 0, "id": 1}))
        elif option is 'PHOTO':
            return list(self.users.find(query, {"_id": 0, "location": 0, "range": 0}))


    def nearbyBuilding(self, u_id):
        user_list = []
        building_list = self.containingBuildings(u_id)
        for b in building_list:
            user_list.extend(self.insideBuilding(b["id"], True, u_id, "PHOTO"))
        return user_list


    def sendMessage(self, u_id, message, method):
        to_list = []
        building_list = []
        if method is "nearby":
            to_list = self.nearbyUsers(u_id, 'IDS')
        elif method is "building":
            to_list = []
            building_list = self.containingBuildings(u_id)
            for b in building_list:
                to_list.extend(self.insideBuilding(b["id"], True, u_id, "IDS"))
        else:
            pass
        if not to_list:
            pass
        else:
            self.message_id = self.message_id + 1
            self.messages.insert_one({"message": message, "id": self.message_id, "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            for destination in to_list:
                message = {"from": u_id, "to": destination["id"], "id": self.message_id, "rcv": 0}
                # if message was sent to entire building then saves building id in message
                if method is "building":
                    message["buildings"] = [building['id'] for building in building_list]
                self.message_table.insert_one(message)

    def getNewMessages(self, u_id):
        new_messages_results = list(self.message_table.find({"to": u_id, "rcv": 0}, {"id": 1, "from": 1, "datetime":1}))
        new_messages = []
        for message in new_messages_results:
            content = list(self.messages.find({"id": message["id"]}, {"message": 1, "datetime": 1}))[0]
            new_messages.append({"from": message["from"], "text": content["message"], "datetime": content["datetime"]})
        return new_messages


    def getAllMessages(self, u_id):
        all_messages_results = list(self.message_table.find({"to": u_id}, {"id": 1, "from": 1}))
        all_messages = []
        for message in all_messages_results:
            content = list(self.messages.find({"id": message["id"]}, {"message": 1, "datetime": 1}))[0]
            all_messages.append({"from": message["from"], "text": content["message"], "datetime": content["datetime"]})
        return all_messages

    def showUserMessages(self, u_id):
        all_messages_results = list(self.message_table.find({"$or": [{"to": u_id}, {"from": u_id}]}, {"id": 1, "to":1, "from": 1}))
        all_messages = []
        for message in all_messages_results:
            content = list(self.messages.find({"id": message["id"]}, {"message": 1, "datetime": 1}))[0]
            all_messages.append({"from": message["from"], "to": message["to"], "text": content["message"], "datetime": content["datetime"]})
        return all_messages

    def showBuildingMessages(self, b_id):
        all_messages_results = list(self.message_table.find({"buildings": b_id}, {"id": 1, "to":1, "from": 1}))
        all_messages = []
        last_id = None
        message_index = -1
        for message in all_messages_results:
            if message["id"] is not last_id:
                last_id = message["id"]
                message_index = message_index + 1
                content = list(self.messages.find({"id": message["id"]}, {"_id": 0, "message": 1, "datetime": 1}))[0]
                all_messages.append({"from": message["from"], "to": [message["to"]], "text": content["message"],
                                     "datetime": content["datetime"]})
            else:
                all_messages[message_index]["to"].append(message["to"])
            #content = list(self.messages.find({"id": message["id"]}, {"message": 1, "datetime": 1}))[0]
            #all_messages.append({"from": message["from"], "to": message["to"], "text": content["message"], "datetime": content["datetime"]})
        return all_messages


    def showAllMessages(self):
        all_messages_results = list(self.message_table.find({}, {"_id": 0, "id": 1, "to":1, "from": 1}))
        print(all_messages_results)
        all_messages = []
        last_id = None
        message_index = -1
        for message in all_messages_results:
            if message["id"] is not last_id:
                last_id = message["id"]
                message_index = message_index + 1
                content = list(self.messages.find({"id": message["id"]}, {"_id": 0, "message": 1, "datetime": 1}))[0]
                all_messages.append({"from": message["from"], "to": [message["to"]], "text": content["message"],
                                     "datetime": content["datetime"]})
            else:
                all_messages[message_index]["to"].append(message["to"])
            #print(content)
            #all_messages.append({"from": message["from"], "to": message["to"], "text": content["message"], "datetime": content["datetime"]})
        return all_messages


    def messagesReceived(self, u_id):
        self.message_table.update_many({"to": u_id}, {"$set": {"rcv": 1}})
