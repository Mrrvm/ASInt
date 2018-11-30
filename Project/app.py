from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import appDB
import json

app = Flask(__name__)


@app.route('/API/addValue', methods=['POST'])
def addValue():
    if request.json["number"] == None:
        pass
    else:
        d = request.json["number"]
        print(d)
    return jsonify()


if __name__ == '__main__':
    app.run()