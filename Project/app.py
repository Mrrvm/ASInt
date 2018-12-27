from flask import Flask
from blueprints.cache.cache import cache
from blueprints.user.appUser import appUser
from blueprints.admin.appAdmin import appAdmin
import appDB

app = Flask(__name__)
cache.init_app(app, config={'CACHE_TYPE': 'simple'})
db = appDB.appDB()
app.register_blueprint(appUser)
app.register_blueprint(appAdmin)

if __name__ == '__main__':
    app.run()
