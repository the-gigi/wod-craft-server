from api import api
import resources


# Routing
def map_routes():
    api.add_resource(resources.Activity, '/api/v1.0/activity/<int:id>', endpoint='activity')
    api.add_resource(resources.Activities, '/api/v1.0/activities', endpoint='activities')
    api.add_resource(resources.Score, '/api/v1.0/score/<int:id>', endpoint='score')
    api.add_resource(resources.Scores, '/api/v1.0/scores', endpoint='scores')
