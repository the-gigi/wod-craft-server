from datetime import datetime
from flask import request
from flask.ext.restful import Resource, abort
from flask.ext.restful.reqparse import RequestParser
from wodcraft.api.serializers import (ActivitySerializer,
                                      ScoreSerializer,
                                      TagSerializer,
                                      UserSerializer)
from wodcraft.api import models

# Will be set by api.create_app()
db = None


def _process_tags(tags, user_id):
    """Create non-existing tags and return list of Tag models"""

    # get current tags
    q = db.session.query
    user_tags = q(models.Tag).filter_by(user_id=user_id)

    # If no change is required just bail out and return current list
    if set(tags) == set([t.tag for t in user_tags]):
        return tags

    if not tags:
        return []

    result = []

    for t in tags:
        tag = q(models.Tag).filter_by(user_id=user_id, tag=t).scalar()
        if not tag:
            tag = Tag(tag=t, user_id=user_id)
            db.session.add(tag)
        result.append(tag)
    return result


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
    def get(self, id):
        q = db.session.query
        result = q(models.Score).get(id)
        result = ScoreSerializer(result).data
        return {'result': result}

    def put(self, id):
        """Update tags for a score"""
        parser = RequestParser()
        parser.add_argument('tags', type=str, required=True)
        args = parser.parse_args()

        q = db.session.query
        score = q(models.Score).get(id)

        tag_names = [t.strip() for t in args.tags.split(',')]

        score.tags = _process_tags(tag_names, score.user_id)
        db.session.commit()
        score = q(models.Score).get(id)
        result = ScoreSerializer(score).data
        return {'result': result}

    def delete(self, id):
        pass


class Scores(Resource):
    def get(self):
        q = db.session.query
        result = q(models.Score).all()
        result = [ScoreSerializer(r).data for r in result]
        return {'result': result}

    def post(self):
        """Post a new score"""
        try:
            r = request.values
            # Verify all required arguments supplied
            required = 'activity_id user_id when rx'.split()
            for x in required:
                if not x in r.keys():
                    abort(400)

            # Verify that exactly one of weight, reps or time is provided
            if len(set(r.keys()) & set(['weight', 'reps', 'time'])) != 1:
                abort(400)

            s = models.Score()
            s.activity_id = r['activity_id']
            s.user_id = r['user_id']
            s.when = datetime.strptime(r['when'], '%Y-%m-%d').date()
            s.rx = r['rx'].lower() in (1, 'true')
            s.weight = r.get('weight', None)
            s.reps = r.get('reps', None)
            s.time = r.get('time', None)
            s.tags = _process_tags(r.get('tags', []), r['user_id'])
            db.session.add(s)
            db.session.commit()

            result = ScoreSerializer(s).data
            return {'result': result}
        except Exception as e:
            raise


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
