import resources


# Routing
def map_routes(api):
    api.add_resource(resources.Activity,
                     '/api/v1.0/activity/<int:id>',
                     endpoint='activity')
    api.add_resource(resources.Activities,
                     '/api/v1.0/activities',
                     endpoint='activities')
    api.add_resource(resources.Score,
                     '/api/v1.0/score/<int:id>',
                     endpoint='score')
    api.add_resource(resources.Scores,
                     '/api/v1.0/scores',
                     endpoint='scores')

    api.add_resource(resources.Tag,
                     '/api/v1.0/tag/<int:id>',
                     endpoint='tag')

    api.add_resource(resources.Tags,
                     '/api/v1.0/tags',
                     endpoint='tags')

    api.add_resource(resources.User,
                     '/api/v1.0/user/<int:id>',
                     endpoint='user')

    api.add_resource(resources.Users,
                     '/api/v1.0/users',
                     endpoint='users')
