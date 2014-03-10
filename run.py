#!flask/bin/python
from api import app
from api.routes import map_routes

map_routes()

app.run(port=8888, debug=True)
