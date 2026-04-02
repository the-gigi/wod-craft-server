from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from wodcraft.api.routes import map_routes
from wodcraft.api import resources
from flask import Flask
from flask_restful import Api


def create_app(debug=True, testing=False):
    app = Flask(__name__)
    app.config.from_object('wodcraft.api.config')

    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    resources.db = app.db = SQLAlchemy(app)
    api = Api(app)
    map_routes(api)

    if debug and not testing:
        CORS(app)

    return app
