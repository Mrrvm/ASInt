from flask import Blueprint
from flask import render_template
from flask import request
from flask import make_response
from flask import redirect
from flask import url_for
import requests
import jwt
import uuid
import appDB

appUser = Blueprint('appUser', __name__, template_folder='templates', static_url_path='/blueprints/user/static', static_folder='./static')

db = appDB.appDB()
SECRET_KEY_USER = uuid.uuid4().hex
fenixEdu_ClientId = "1695915081465915"
fenixEdu_redirectURL = "http://127.0.0.1:5000/users/auth"
fenixEdu_ClientSecret = "xCzg7GMrhRI5ncklUy+wN3fl6UOdjHKVhUlWWaT5Ibm/PTbS5TEkJsmt5F62IwTXnZ5xGcqeMeia7K021Mtm6g=="
DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = "5000"
DEFAULT_LAT = "38.73"
DEFAULT_LONG = "-9.14"
DEFAULT_RANGE = "10"

@appUser.route('/')
def init():
    return homeUser()

@appUser.route('/home/')
def homeUser():
    print("hi")
    return render_template("home.html")


@appUser.route('/user/login', methods=['GET'])
def loginUser():
    redirect_url = "https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id="
    redirect_url = redirect_url + fenixEdu_ClientId + "&redirect_uri=" + fenixEdu_redirectURL
    return redirect(redirect_url)

@appUser.route('/users/auth', methods=['GET'])
def authUser():
    code = request.args.get("code")
    request_url_access_token = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'
    request_data = {'client_id': fenixEdu_ClientId, 'client_secret': fenixEdu_ClientSecret,
                    'redirect_uri': fenixEdu_redirectURL, 'code': code, 'grant_type': 'authorization_code'}
    request_access_token = requests.post(request_url_access_token, data=request_data)
    access_token = request_access_token.json()['access_token']
    get_info_params = {'access_token': access_token}
    request_url_info = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person"
    request_info = requests.get(request_url_info, params=get_info_params)
    u_id = request_info.json()['username']
    u_name = request_info.json()['name']
    u_photo = request_info.json()['photo']
    db.addUser(u_id, DEFAULT_LAT, DEFAULT_LONG, DEFAULT_RANGE, u_name, u_photo['data'])
    resp = make_response(redirect(url_for('appUser.loggedUser', id=u_id)))
    u_token = jwt.encode({'u_id': u_id}, SECRET_KEY_USER, algorithm='HS256').decode('utf-8')
    resp.set_cookie('token', u_token)
    return resp



@appUser.route('/user/<id>')
def loggedUser(id):
    token = request.cookies.get('token')
    payload = jwt.decode(token, SECRET_KEY_USER, algorithms=['HS256'])
    print(payload['u_id'])
    if id != payload['u_id']:
        return redirect(url_for('appUser.homeUser'))
    u_data = db.getUser(id)[0] #TODO: add cache here
    u_name = u_data['name']
    u_photo = u_data['photo']
    u_location = u_data['location']
    u_lat = u_location['coordinates'][1]
    u_long = u_location['coordinates'][0]
    return render_template("user.html", name=u_name, photo=u_photo, userid=id, lat=u_lat, long=u_long)


@appUser.route('/user/<id>/location', methods=['POST'])
def defineLocation(id):
    lat = request.form["lat"]
    long = request.form["long"]
    db.defineLocation(id, lat, long)
    return redirect(url_for('appUser.loggedUser', id=id))


@appUser.route('/user/<id>/nearby', methods=['GET'])
def nearbyUsers(id):
    nearby = db.nearbyUsers(id)
    print(nearby)
    # do something with building list
    return redirect(url_for('appUser.loggedUser', id=id))


@appUser.route('/user/<id>/buildings', methods=['GET'])
def insideBuilding(id):
    buildings = db.insideBuilding(id)
    print(buildings)
    # do something with building list
    return redirect(url_for('appUser.loggedUser', id=id))