from flask.ext.sqlalchemy import SQLAlchemy
from routes import map_routes
import resources

# from config import (basedir,
#                     ADMINS,
#                     MAIL_SERVER,
#                     MAIL_PORT,
#                     MAIL_USERNAME,
#                     MAIL_PASSWORD)
from flask import Flask
from flask.ext.restful import Api


def create_app():
    app = Flask(__name__)
    app.config.from_object('api.config')
    resources.db = app.db = SQLAlchemy(app)
    api = Api(app)
    map_routes(api)

    return app





