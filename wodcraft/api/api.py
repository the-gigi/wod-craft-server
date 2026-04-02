from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from wodcraft.api.routes import map_routes
from wodcraft.api import resources
from flask import Flask
from flask_restful import Api


def create_app(debug=True):
    app = Flask(__name__)
    app.config.from_object('wodcraft.api.config')
    resources.db = app.db = SQLAlchemy(app)
    api = Api(app)
    map_routes(api)

    if debug:
        CORS(app)

    return app
