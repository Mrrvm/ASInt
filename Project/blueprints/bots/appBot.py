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

appAdmin = Blueprint('appBot', __name__, template_folder='templates')

db = appDB.appDB()
DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = "5000"
DEFAULT_LAT = "38.73"
DEFAULT_LONG = "-9.14"
DEFAULT_RANGE = "10"

@appAdmin.route('/bot', methods=['POST'])
def botMessage():
    bot_id = request.json["id"]
    key_1 = request.json["key"]
    key_2 = db.botKey(bot_id)
    # THIS IS WRONG
    if key_1 == key_2:
        pass
    else:
        pass

