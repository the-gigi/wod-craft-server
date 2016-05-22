#!flask/bin/python
from wodcraft.api.api import create_app

debug = True

app = create_app(debug=debug)

app.run(port=8888, debug=debug)
