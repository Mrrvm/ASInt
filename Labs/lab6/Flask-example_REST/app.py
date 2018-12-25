from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

class Storage:
    def __init__ (self):
        self.data = {}
    def getSize(self):
        return len(self.data)
    def store(self, val):
        try:
            self.data[val] += 1
        except:
            self.data[val] = 1
    def getKeys(self):
        return self.data.keys()
    def getValue(self, key):
        try:
            return self.data[key]
        except:
            return None

app = Flask(__name__)
st = Storage()


@app.route('/')
def hello_world():
    s = st.getSize()
    ks = st.getKeys()
    return render_template("mainPage.html", counter = s, keys = ks)

@app.route('/addValue', methods=['POST'])
def add_Value():
    s = str(request.form)
    if request.form["val"]== None:
        pass
    else:
        val = request.form["val"]
        st.store(val)
    s = st.getSize()
    return hello_world()

@app.route('/API/addValue', methods=['POST'])
def API_add_Value():
    if request.json["number"] == None:
        pass
    else:
        val = request.json["number"]
        st.store(val)
    s = st.getSize()
    return jsonify()

@app.route('/value/<key>')
def get_Value(key):
    val = st.getValue(key)
    if val == None:
        return render_template("errorPage.html", name = request.args["key"])
    return str(val)

@app.route('/API/value/<key>', methods=['GET'])
def API_get_Value(key):
    val = st.getValue(key)
    if val == None:
        return jsonify("Error")
    return val


@app.route('/getValue')
def get_Value2():
    key = str(request.args["key"])
    return get_Value(key)



if __name__ == '__main__':

    app.run()
