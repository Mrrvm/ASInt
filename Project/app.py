from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import appDB
import json

app = Flask(__name__)
db = appDB.appDB()


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

@app.route('/users/newuser', methods=['POST'])
def addUser():
    u_id = request.json["id"]
    u_lat = request.json["lat"]
    u_long = request.json["long"]
    if u_id == None or u_lat == None or u_long == None:
        pass
    else:
        db.addUser(str(u_id), int(u_lat), int(u_long))
        return '', 204


@app.route('/admin/users/<id>', methods=['GET'])
def single_user(id):
    user = db.showUser(str(id))
    return jsonify(user.__dict__)

if __name__ == '__main__':
    app.run()