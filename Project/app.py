from flask import Flask
from blueprints.cache.cache import cache
from blueprints.user.appUser import appUser
from blueprints.admin.appAdmin import appAdmin
from blueprints.bots.appBot import appBot


app = Flask(__name__)
cache.init_app(app, config={'CACHE_TYPE': 'simple'})
app.register_blueprint(appUser)
app.register_blueprint(appAdmin)
app.register_blueprint(appBot)

if __name__ == '__main__':
    app.run()
