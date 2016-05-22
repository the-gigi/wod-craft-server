from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
from wodcraft.api.routes import map_routes
from wodcraft.api import resources

# from config import (basedir,
#                     ADMINS,
#                     MAIL_SERVER,
#                     MAIL_PORT,
#                     MAIL_USERNAME,
#                     MAIL_PASSWORD)
from flask import Flask
from flask.ext.restful import Api


def create_app(debug=True):
    app = Flask(__name__)
    app.config.from_object('wodcraft.api.config')
    resources.db = app.db = SQLAlchemy(app)
    api = Api(app)
    map_routes(api)

    if debug:
        CORS(app)

    return app





