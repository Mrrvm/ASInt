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

appBot = Blueprint('appBot', __name__, template_folder='templates')

db = appDB.appDB()

@appBot.route('/bot', methods=['POST'])
def botMessage():
    bot_id = request.json["id"]
    key_1 = request.json["key"]
    key_2 = db.botKey(bot_id)
    if key_1 == key_2:
        bot_message = request.json["message"]
        db.botMessage(bot_id, bot_message)
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error"})

