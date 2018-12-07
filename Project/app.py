from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
import requests

import appDB
import json

app = Flask(__name__)
db = appDB.appDB()

FenixEdu_ClientId = "1695915081465915"
FenixEdu_redirectURL = "http://127.0.0.1:5000/users/auth"
FenixEdu_ClientSecret = "xCzg7GMrhRI5ncklUy+wN3fl6UOdjHKVhUlWWaT5Ibm/PTbS5TEkJsmt5F62IwTXnZ5xGcqeMeia7K021Mtm6g=="

DEFAULT_LAT = 38.73
DEFAULT_LONG = -9.14

@app.route('/admin/buildings', methods=['GET'])
def showBuildings():
    buildings = db.showAllBuildings()
    return jsonify([ob.__dict__ for ob in buildings])

@app.route('/admin/buildings/add', methods=['POST'])
def addBuilding():
    b_name = request.json["name"]
    b_id = request.json["id"]
    b_lat = request.json["lat"]
    b_long = request.json["long"]
    if b_name == None or b_id == None or b_lat == None or b_long == None:
        pass
    else:
        db.addBuilding(b_name, int(b_lat), int(b_long), int(b_id))
        return '', 204

@app.route('/admin/buildings/remove', methods=['POST'])
def removeBuilding():
    b_id = request.form["id"]
    if b_id == None:
        pass
    else:
        db.removeBuilding(int(b_id))
        return '', 204

@app.route('/admin/buildings/<id>', methods=['GET'])
def single_building(id):
    building = db.showBuilding(int(id))
    return jsonify(building.__dict__)


@app.route('/admin/users', methods=['GET'])
def showUsers():
    users = db.showAllUsers()
    return jsonify([ob.__dict__ for ob in users])


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
    db.addUser(str(u_id), DEFAULT_LAT, DEFAULT_LONG)
    return '', 204

@app.route('/admin/users/<id>', methods=['GET'])
def single_user(id):
    user = db.showUser(str(id))
    return jsonify(user.__dict__)

if __name__ == '__main__':
    app.run()