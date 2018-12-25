from flask import Flask
from blueprints.user.appUser import appUser
from blueprints.admin.appAdmin import appAdmin

app = Flask(__name__)
app.register_blueprint(appUser)
app.register_blueprint(appAdmin)

if __name__ == '__main__':
    app.run()
