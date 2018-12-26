"""
appAdmin.py
Contains the following user routes
/admin/login
/admin/buildings
/admin/buildings/add
/admin/buildings/remove
/admin/buildings/<id>
/admin/users
/admin/users/<id>
"""

from flask import Blueprint
from flask import request
from flask import jsonify
import appDB

appAdmin = Blueprint('appAdmin', __name__, template_folder='templates')

db = appDB.appDB()
DEFAULT_IP = "127.0.0.1"
DEFUALT_PORT = "5000"
DEFAULT_LAT = "38.73"
DEFAULT_LONG = "-9.14"
DEFAULT_RANGE = "10"
admin_login = {"username": "admin", "password": "123", "key": "1M4KAH19PO"}


@appAdmin.route('/admin/login', methods=['POST'])
def adminLogin():
    username = request.json["username"]
    password = request.json["password"]
    if username == admin_login['username'] and password == admin_login['password']:
        return jsonify({"status": "logged successfully", "key": admin_login['key']})
    else:
        return jsonify({"status": "error during login"})

@appAdmin.route('/admin/buildings', methods=['GET'])
def showBuildings():
    admin_key = request.json["key"]
    if admin_key != admin_login['key']:
        return jsonify({"status": "not logged in"})
    else:
        buildings = db.showAllBuildings()
        return jsonify(buildings)

@appAdmin.route('/admin/buildings/add', methods=['POST'])
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

@appAdmin.route('/admin/buildings/remove', methods=['POST'])
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

@appAdmin.route('/admin/buildings/<id>', methods=['GET'])
def single_building(id):
    admin_key = request.json["key"]
    if admin_key != admin_login['key']:
        return jsonify({"status": "not logged in"})
    else:
        building = db.showBuilding(id)
        return jsonify(building)


@appAdmin.route('/admin/users', methods=['GET'])
def showUsers():
    admin_key = request.json["key"]
    if admin_key != admin_login['key']:
        return jsonify({"status": "not logged in"})
    else:
        users = db.showAllUsers()
        return jsonify(users)


@appAdmin.route('/admin/users/<id>', methods=['GET'])
def single_user(id):
    admin_key = request.json["key"]
    if admin_key != admin_login['key']:
        return jsonify({"status": "not logged in"})
    else:
        user = db.showUser(id)
        return jsonify(user)

@appAdmin.route('/admin/bots', methods=['GET'])
def showBots():
    admin_key = request.json["key"]
    if admin_key != admin_login['key']:
        return jsonify({"status": "not logged in"})
    else:
        bots = db.showAllBots()
        return jsonify(bots)

@appAdmin.route('/admin/bots/new', methods=['POST'])
def newBot():
    admin_key = request.json["key"]
    if admin_key != admin_login['key']:
        return jsonify({"status": "not logged in"})
    else:
        allowed_buildings = request.json["buildings"]
        bot = db.newBot(allowed_buildings)
        return jsonify(bot)

@appAdmin.route('/admin/bots/delete', methods=['POST'])
def deleteBot():
    admin_key = request.json["key"]
    if admin_key != admin_login['key']:
        return jsonify({"status": "not logged in"})
    else:
        bot_id = request.json["id"]
        db.deleteBot(bot_id)
        return '', 204