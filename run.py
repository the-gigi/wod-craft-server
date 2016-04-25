#!flask/bin/python
from wodcraft.api.api import create_app

app = create_app()

app.run(port=8888, debug=True)
