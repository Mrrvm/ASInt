import requests


def login():
    print("Login")
    username = input("Username:")
    password = input("Password:")
    ToSend = {'username': username, 'password': password}
    r = requests.post('http://127.0.0.1:5000/admin/login', json=ToSend)
    login_response = r.json()
    if login_response['status'] == "error during login":
        print("Wrong credentials")
        exit(0)
    key = login_response['key']
    print("Welcome " + username)
    return username, key


def buildings(endpoint, key):
    print("Choose one of the following:")
    command = input("AddBuilding  ListAll  ShowBuilding  RemoveBuilding:\n")
    if command.upper() == "ADDBUILDING":
        building_data = input('Insert NAME, ID, LATITUDE, LONGITUDE (separated by ,):\n')
        b = building_data.split(',')
        ToSend = {'name': b[0], 'id': b[1], 'lat': b[2], 'long': b[3], 'key': key}
        r = requests.post(endpoint + "/add", json=ToSend)
    elif command.upper() == "LISTALL":
        ToSend = {'key': key}
        r = requests.get(endpoint, json=ToSend)
        print(r.json())
    elif command.upper() == "SHOWBUILDING":
        b_id = input("Building id: ")
        ToSend = {'key': key}
        r = requests.get(endpoint + "/" + b_id, json=ToSend)
        print(r.json())
    elif command.upper() == "REMOVEBUILDING":
        b_id = input("Building id: ")
        ToSend = {'id': b_id, 'key': key}
        r = requests.post(endpoint + "/remove", json=ToSend)


def users(endpoint, key):
    print("Choose one of the following:")
    command = input("ListAll  ShowUser:\n")
    if command.upper() == "LISTALL":
        ToSend = {'key': key}
        r = requests.get(endpoint, json=ToSend)
        user_list = r.json()
        for u in user_list:
            print("ID: " + u['id'] + " Name: " + u['name'])
    elif command.upper() == "SHOWUSER":
        u_id = input("User id: ")
        ToSend = {'key': key}
        r = requests.get(endpoint + "/" + u_id, json=ToSend)
        user = r.json()
        for key, val in user[0].items():
            print(key + ": " + str(val))


if __name__ == '__main__':
    username, key = login()
    while(1):
        print("Choose one of the following:")
        command = input("Buildings  Users  Quit:\n")
        endpoint = "http://127.0.0.1:5000/admin"
        if command.upper() == "BUILDINGS":
            buildings(endpoint + "/buildings", key)
        elif command.upper() == "USERS":
            users(endpoint + "/users", key)
        elif command.upper() == "QUIT":
            print("Goodbye " + username)
            exit(0)