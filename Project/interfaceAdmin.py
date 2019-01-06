import requests

# endpoint = "https://elegant-folder-226910.appspot.com/admin"
endpoint = "http://127.0.0.1:5000/admin"

def login(endpoint):
    print("Login")
    username = input("Username:")
    password = input("Password:")
    toSend = {'username': username, 'password': password}
    r = requests.post(endpoint + '/login', json=toSend)
    login_response = r.json()
    if login_response['status'] == "error during login":
        print("Wrong credentials")
        exit(0)
    key = login_response['key']
    print("Welcome " + username)
    return username, key


def buildings(endpoint, key):
    print("\nChoose one of the following:")
    u_input = input("[1]AddBuilding  [2]ListAll  [3]ShowBuilding  [4]UsersInBuilding  [5]RemoveBuilding\n")
    if u_input == "1":
        building_data = input('Insert NAME, ID, LATITUDE, LONGITUDE (separated by ,):\n')
        b = building_data.split(',')
        toSend = {'name': b[0], 'id': b[1], 'lat': b[2], 'long': b[3], 'key': key}
        r = requests.post(endpoint + "/add", json=toSend)
    elif u_input == "2":
        toSend = {'key': key}
        r = requests.post(endpoint, json=toSend)
        b_list = r.json()
        for b in b_list:
            print("ID: " + b['id'] + " Name: " + b['name'])
    elif u_input == "3":
        b_id = input("Building id: ")
        toSend = {'key': key}
        r = requests.post(endpoint + "/" + b_id, json=toSend)
        building = r.json()
        for key, val in building.items():
            print(key + ": " + str(val))
    elif u_input == "4":
        b_id = input("Building id: ")
        toSend = {'key': key}
        r = requests.post(endpoint + "/" + b_id + "/users", json=toSend)
        user_list = r.json()
        users = [user['id'] for user in user_list]
        for u in users:
            print("ID: " + u)
    elif u_input == "5":
        b_id = input("Building id: ")
        toSend = {'id': b_id, 'key': key}
        r = requests.post(endpoint + "/remove", json=toSend)


def users(endpoint, key):
    print("\nChoose one of the following:")
    u_input = input("[1]ListAll  [2]ShowUser\n")
    if u_input == "1":
        toSend = {'key': key}
        r = requests.post(endpoint, json=toSend)
        user_list = r.json()
        for u in user_list:
            print("ID: " + u['id'] + " Name: " + u['name'])
    elif u_input == "2":
        u_id = input("User id: ")
        toSend = {'key': key}
        r = requests.post(endpoint + "/" + u_id, json=toSend)
        user = r.json()
        for key, val in user.items():
            print(key + ": " + str(val))

def bots(endpoint, key):
    print("\nChoose one of the following:")
    u_input = input("[1]ListAll  [2]NewBot  [3]DeleteBot\n")
    if u_input == "1":
        toSend = {'key': key}
        r = requests.post(endpoint, json=toSend)
        bot_list = r.json()
        for bot in bot_list:
            print("ID: " + str(bot['id']) + " Key: " + bot['key'] + " Buildings: " + str(bot['buildings']))
    elif u_input == "2":
        allowed_buildings = input("Insert buildings ID1,ID2,...IDn (separated by ,):\n").split(',')
        toSend = {'key': key, 'buildings': allowed_buildings}
        r = requests.post(endpoint + "/new", json=toSend)
        new_bot = r.json()
        for key, val in new_bot.items():
            print(key + ": " + str(val))
    elif u_input == "3":
        bot_id = input("Bot id: ")
        toSend = {'id': bot_id, 'key': key}
        r = requests.post(endpoint + "/delete", json=toSend)

def logs(endpoint, key):
    print("\nChoose one of the following:")
    u_input = input("[1]All  [2]ByUser  [3]ByBuilding\n")
    if u_input == "1":
        u_input = input("[1]AllMovements  [2]AllMessages\n")
        if u_input == "1":
            toSend = {'key': key}
            r = requests.post(endpoint + "/movements", json=toSend)
            movement_list = r.json()
            for move in movement_list:
                print("\nMovement:")
                for key, val in move.items():
                    print(key + ": " + str(val))
            #print(movement_list)
        elif u_input == "2":
            toSend = {'key': key}
            r = requests.post(endpoint + "/messages", json=toSend)
            message_list = r.json()
            for message in message_list:
                print("\nMessage:")
                for key, val in message.items():
                    print(key + ": " + str(val))
    elif u_input == "2":
        user_id = input("User id: ")
        u_input = input("[1]UserMovements  [2]UserMessages\n")
        if u_input == "1":
            toSend = {'key': key}
            r = requests.post(endpoint + "/movements/user/" + user_id, json=toSend)
            movement_list = r.json()
            for move in movement_list:
                print("\nMovement:")
                for key, val in move.items():
                    print(key + ": " + str(val))
        elif u_input == "2":
            toSend = {'key': key}
            r = requests.post(endpoint + "/messages/user/" + user_id, json=toSend)
            message_list = r.json()
            for message in message_list:
                print("\nMessage:")
                for key, val in message.items():
                    print(key + ": " + str(val))
    elif u_input == "3":
        building_id = input("Building id: ")
        toSend = {'key': key}
        r = requests.post(endpoint + "/messages/building/" + building_id, json=toSend)
        message_list = r.json()
        for message in message_list:
            print("\nMessage:")
            for key, val in message.items():
                print(key + ": " + str(val))


if __name__ == '__main__':
    username, key = login(endpoint)
    while(1):
        print("\nChoose one of the following:")
        u_input = input("[1]Buildings  [2]Users  [3]Bots  [4]Logs  [5]Quit\n")
        if u_input == "1":
            buildings(endpoint + "/buildings", key)
        elif u_input == "2":
            users(endpoint + "/users", key)
        elif u_input == "3":
            bots(endpoint + "/bots", key)
        elif u_input == "4":
            logs(endpoint + "/logs", key)
        elif u_input == "5":
            print("Goodbye " + username)
            exit(0)