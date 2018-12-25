import requests


def login():
    print("Login")
    username = input("Username:")
    password = input("Password:")
    toSend = {'username': username, 'password': password}
    r = requests.post('http://127.0.0.1:5000/admin/login', json=toSend) #TODO change IP to any
    login_response = r.json()
    if login_response['status'] == "error during login":
        print("Wrong credentials")
        exit(0)
    key = login_response['key']
    print("Welcome " + username)
    return username, key


def buildings(endpoint, key):
    print("\nChoose one of the following:")
    u_input = input("[1]AddBuilding  [2]ListAll  [3]ShowBuilding  [4]RemoveBuilding:\n")
    if u_input == "1":
        building_data = input('Insert NAME, ID, LATITUDE, LONGITUDE (separated by ,):\n')
        b = building_data.split(',')
        toSend = {'name': b[0], 'id': b[1], 'lat': b[2], 'long': b[3], 'key': key}
        r = requests.post(endpoint + "/add", json=toSend)
    elif u_input == "2":
        toSend = {'key': key}
        r = requests.get(endpoint, json=toSend)
        b_list = r.json()
        for b in b_list:
            print("ID: " + b['id'] + " Name: " + b['name'])
    elif u_input == "3":
        b_id = input("Building id: ")
        toSend = {'key': key}
        r = requests.get(endpoint + "/" + b_id, json=toSend)
        building = r.json()
        print(building)
    elif u_input == "4":
        b_id = input("Building id: ")
        toSend = {'id': b_id, 'key': key}
        r = requests.post(endpoint + "/remove", json=toSend)


def users(endpoint, key):
    print("\nChoose one of the following:")
    u_input = input("[1]ListAll  [2]ShowUser:\n")
    if u_input == "1":
        toSend = {'key': key}
        r = requests.get(endpoint, json=toSend)
        user_list = r.json()
        for u in user_list:
            print("ID: " + u['id'] + " Name: " + u['name'])
    elif u_input == "2":
        u_id = input("User id: ")
        toSend = {'key': key}
        r = requests.get(endpoint + "/" + u_id, json=toSend)
        user = r.json()
        for key, val in user.items():
            print(key + ": " + str(val))


if __name__ == '__main__':
    username, key = login()
    while(1):
        print("\nChoose one of the following:")
        u_input = input("[1]Buildings  [2]Users  [3]Quit\n")
        endpoint = "http://127.0.0.1:5000/admin"
        if u_input == "1":
            buildings(endpoint + "/buildings", key)
        elif u_input == "2":
            users(endpoint + "/users", key)
        elif u_input == "3":
            print("Goodbye " + username)
            exit(0)