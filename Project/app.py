from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import redirect
from flask import jsonify
from flask import url_for
import requests
import jwt
import uuid
import appDB
import json

app = Flask(__name__)
db = appDB.appDB()

DEFAULT_IP = "127.0.0.1:5000"
FenixEdu_ClientId = "1695915081465915"
FenixEdu_redirectURL = "http://127.0.0.1:5000/users/auth"
FenixEdu_ClientSecret = "xCzg7GMrhRI5ncklUy+wN3fl6UOdjHKVhUlWWaT5Ibm/PTbS5TEkJsmt5F62IwTXnZ5xGcqeMeia7K021Mtm6g=="

DEFAULT_LAT = "38.73"
DEFAULT_LONG = "-9.14"
DEFAULT_RANGE = "10"

SECRET_KEY_USER = uuid.uuid4().hex

admin_login = {"username": "admin", "password": "123", "key": "1M4KAH19PO"}


@app.route('/admin/login', methods=['POST'])
def adminLogin():
    username = request.json["username"]
    password = request.json["password"]
    if username == admin_login['username'] and password == admin_login['password']:
        return jsonify({"status": "logged successfully", "key": admin_login['key']})
    else:
        return jsonify({"status": "error during login"})

@app.route('/admin/buildings', methods=['GET'])
def showBuildings():
    admin_key = request.json["key"]
    if admin_key != admin_login['key']:
        return jsonify({"status": "not logged in"})
    else:
        buildings = db.showAllBuildings()
        return jsonify(buildings)

@app.route('/admin/buildings/add', methods=['POST'])
def addBuilding():
    admin_key = request.json["key"]
    if admin_key != admin_login['key']:
        return jsonify({"status": "not logged in"})
    else:
        b_name = request.json["name"]
        b_id = request.json["id"]
        b_lat = request.json["lat"]
        b_long = request.json["long"]
        if b_name == None or b_id == None or b_lat == None or b_long == None:
            pass
        else:
            db.addBuilding(b_name, b_lat, b_long, b_id)
            return '', 204

@app.route('/admin/buildings/remove', methods=['POST'])
def removeBuilding():
    admin_key = request.json["key"]
    if admin_key != admin_login['key']:
        return jsonify({"status": "not logged in"})
    else:
        b_id = request.json["id"]
        if b_id == None:
            pass
        else:
            db.removeBuilding(b_id)
            return '', 204

@app.route('/admin/buildings/<id>', methods=['GET'])
def single_building(id):
    admin_key = request.json["key"]
    if admin_key != admin_login['key']:
        return jsonify({"status": "not logged in"})
    else:
        building = db.showBuilding(id)
        return jsonify(building)


@app.route('/admin/users', methods=['GET'])
def showUsers():
    admin_key = request.json["key"]
    if admin_key != admin_login['key']:
        return jsonify({"status": "not logged in"})
    else:
        users = db.showAllUsers()
        return jsonify(users)


@app.route('/admin/users/<id>', methods=['GET'])
def single_user(id):
    admin_key = request.json["key"]
    if admin_key != admin_login['key']:
        return jsonify({"status": "not logged in"})
    else:
        user = db.showUser(id)
        return jsonify(user)


@app.route('/users/login', methods=['GET'])
def loginUser():
    redirect_url = "https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id="
    redirect_url = redirect_url + FenixEdu_ClientId + "&redirect_uri=" + FenixEdu_redirectURL
    return redirect(redirect_url)

@app.route('/users/auth', methods=['GET'])
def authUser():
    code = request.args.get("code")
    request_url_access_token = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'
    request_data = {'client_id': FenixEdu_ClientId, 'client_secret': FenixEdu_ClientSecret,
                    'redirect_uri': FenixEdu_redirectURL, 'code': code, 'grant_type': 'authorization_code'}
    request_access_token = requests.post(request_url_access_token, data=request_data)
    access_token = request_access_token.json()['access_token']
    get_info_params = {'access_token': access_token}
    request_url_info = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person"
    request_info = requests.get(request_url_info, params=get_info_params)
    u_id = request_info.json()['username']
    u_name = request_info.json()['name']
    u_photo = request_info.json()['photo']
    db.addUser(u_id, DEFAULT_LAT, DEFAULT_LONG, DEFAULT_RANGE, u_name, u_photo['data'])
    resp = make_response(redirect(url_for('loggedUser', id=u_id)))
    u_token = jwt.encode({'u_id': u_id}, SECRET_KEY_USER, algorithm='HS256').decode('utf-8')
    resp.set_cookie('token', u_token)
    return resp

@app.route('/home/')
def homeUser():
    return render_template("home.html")

@app.route('/user/<id>')
def loggedUser(id):
    token = request.cookies.get('token')
    payload = jwt.decode(token, SECRET_KEY_USER, algorithms=['HS256'])
    print(payload['u_id'])
    if id != payload['u_id']:
        return redirect(url_for('homeUser'))
    u_data = db.getUser(id)[0]
    u_name = u_data['name']
    u_photo = u_data['photo']
    u_location = u_data['location']
    u_lat = u_location['coordinates'][1]
    u_long = u_location['coordinates'][0]
    return render_template("user.html", name=u_name, photo=u_photo, userid=id, lat=u_lat, long=u_long)


@app.route('/user/<id>/location', methods=['POST'])
def defineLocation(id):
    lat = request.form["lat"]
    long = request.form["long"]
    db.defineLocation(id, lat, long)
    return redirect(url_for('loggedUser', id=id))


@app.route('/user/<id>/nearby', methods=['GET'])
def nearbyUsers(id):
    nearby = db.nearbyUsers(id)
    print(nearby)
    # do something with building list
    return redirect(url_for('loggedUser', id=id))


@app.route('/user/<id>/buildings', methods=['GET'])
def insideBuilding(id):
    buildings = db.insideBuilding(id)
    print(buildings)
    # do something with building list
    return redirect(url_for('loggedUser', id=id))

if __name__ == '__main__':
    app.run()