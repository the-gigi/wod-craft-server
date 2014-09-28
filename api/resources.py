from flask import request
from flask.ext.restful import Resource, abort
from serializers import ActivitySerializer, ScoreSerializer, TagSerializer, \
    UserSerializer
import models


# Will be set by api.create_app()
db = None


class User(Resource):
    def get(self, id):
        q = db.session.query
        result = q(models.User).get(id)
        result = UserSerializer(result).data
        return {'result': result}

    def put(self, id):
        pass

    def delete(self, id):
        pass


class Users(Resource):
    def get(self):
        q = db.session.query
        result = q(models.User).get(id)
        result = UserSerializer(result).data
        return {'result': result}

    def post(self):
        q = db.session.query
        name = request.values.get('name', None)
        password = request.values.get('password', None)
        email = request.values.get('email', None)
        if None in (name, password):
            abort(400)  # missing arguments

        if q(models.User).filter_by(name=name).scalar() is not None:
            abort(400)  # existing user
        user = models.User()
        user.name = name
        user.email = email
        user.role = models.ROLE_USER
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        result = UserSerializer(user).data
        return {'result': result}

    def put(self, id):
        pass

    def delete(self, id):
        pass


class Activity(Resource):
    def get(self, id):
        q = db.session.query
        result = q(models.Activity).get(id)
        result = ActivitySerializer(result).data
        return {'result': result}

    def post(self):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


class Activities(Resource):
    def get(self):
        q = db.session.query
        result = q(models.Activity).all()
        result = [ActivitySerializer(r).data for r in result]
        return {'result': result}


class Score(Resource):
    def _process_tags(self, tags, user_id):
        """Create non-existing tags and return list of Tag models"""
        if not tags:
            return []

        result = []
        q = db.session.query
        for t in tags:
            tag = q(models.Tag).filter_by(user_id=user_id, tag=t).scalar()
            if not tag:
                tag = Tag(tag=t, user_id=user_id)
                q.session.add(tag)
            result.append(tag)

        q.session.commit()
        return tags

    def get(self, id):
        q = db.session.query
        result = q(models.Score).get(id)
        result = ScoreSerializer(result).data
        return {'result': result}

    def post(self):
        """Post a new score"""

        r = request.values
        # Verify all required arguments supplied
        required = 'activitiy_id user_id when rx'.split()
        for x in required:
            if not x in r:
                abort(400)

        # Verify that exactly one of weight, reps or time is provided
        if len(set(r.keys()) & set(['weight', 'reps', 'time'])) != 1:
            abort(400)

        s = Score()
        s.activity_id = r['activity_id']
        s.user_id = r['user_id']
        s.when = r['when']
        s.rx = r['rx']
        s.weight = r.get('weight', None)
        s.reps = r.get('reps', None)
        s.time = r.get('time', None)
        s.tags = self._process_tags(r.get('tags', None))
        db.session.add(s)
        db.session.commit()

        result = ScoreSerializer(s).data
        return {'result': result}

    def put(self, id, tag_names):
        """Update tags for a score"""
        q = db.session.query
        score = q(models.Score).get(id)
        m = models.Tag
        all_tags = q(models.Tag).all()
        tags = [t for t in all_tags if t.name in tag_names]
        score.tags = tags
        q.session.commit()

        result = ScoreSerializer(score).data
        return {'result': result}

    def delete(self, id):
        pass


class Scores(Resource):
    def get(self, tags):
        q = db.session.query
        result = q(models.Score).all()
        result = [ScoreSerializer(r).data for r in result]
        return {'result': result}


class Tag(Resource):
    def get(self, id):
        q = db.session.query
        result = q(models.Tag).get(id)
        result = TagSerializer(result).data
        return {'result': result}

    def put(self, id):
        pass

    def delete(self, id):
        pass


class Tags(Resource):
    def get(self):
        q = db.session.query
        result = q(models.Tag).all()
        result = [TagSerializer(r).data for r in result]
        return {'result': result}



'''
#!flask/bin/python

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension."""

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.views import MethodView
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path = "")
api = Api(app)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'message': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}

class TaskListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True, help = 'No task title provided', location = 'json')
        self.reqparse.add_argument('description', type = str, default = "", location = 'json')
        super(TaskListAPI, self).__init__()

    def get(self):
        return { 'tasks': map(lambda t: marshal(t, task_fields), tasks) }

    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'id': tasks[-1]['id'] + 1,
            'title': args['title'],
            'description': args['description'],
            'done': False
        }
        tasks.append(task)
        return { 'task': marshal(task, task_fields) }, 201

class TaskAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('done', type = bool, location = 'json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        task = filter(lambda t: t['id'] == id, tasks)
        if len(task) == 0:
            abort(404)
        return { 'task': marshal(task[0], task_fields) }

    def put(self, id):
        task = filter(lambda t: t['id'] == id, tasks)
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v != None:
                task[k] = v
        return { 'task': marshal(task, task_fields) }

    def delete(self, id):
        task = filter(lambda t: t['id'] == id, tasks)
        if len(task) == 0:
            abort(404)
        tasks.remove(task[0])
        return { 'result': True }

api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint = 'tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<int:id>', endpoint = 'task')

if __name__ == '__main__':
    app.run(debug = True)
'''
