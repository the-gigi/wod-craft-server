import json
from unittest import TestCase
from datetime import datetime, timedelta

from wodcraft.api.api import create_app
from wodcraft.api.models import (
    metadata,
    Activity,
    Score,
    Tag,
    User,
    ROLE_USER,
    ROLE_ADMIN)

from . import test_util


def get_result(response):
    return json.loads(response.data.decode('utf-8'))['result']

class APITest(TestCase):
    def setUp(self):
        """
        """
        # Create in-memory test metadata DB
        self.app = create_app()
        self.session = test_util.create_mem_db(metadata, self.app.db)
        self.test_app = self.app.test_client()

        # Add admin and regular users
        user = User()
        user.name = 'the_gigi'
        user.email = 'the_gigi@gmail.com'
        user.role = ROLE_ADMIN
        self.session.add(user)

        user2 = User()
        user2.name = 'nobody'
        user2.email = 'nobody@aol.com'
        user2.role = ROLE_USER
        self.session.add(user2)

        # Add a few activities
        activities = []
        for i in range(3):
            a = Activity()
            a.name = 'activity_{}'.format(i)
            activities.append(a)
            self.session.add(a)

        # Add a few tags
        tags = []
        for k in range(2):
            t = Tag()
            t.user = user
            t.tag = 'tag_{0}'.format(k)
            tags.append(t)
            self.session.add(t)

        # Add a few scores + tags
        for i in range(3):
            for j in range(2):
                s = Score()
                s.user = user
                s.activity = activities[i]
                s.rx = j == 0
                s.reps = j
                for k in range(j + 1):
                    s.tags.append(tags[k])
                self.session.add(s)
        self.session.commit()

    def tearDown(self):
        """
        """
        self.app.db.restore_engine()
        self.test_app = None

    def test_get_activities_empty(self):
        # Start with a fresh memory db
        self.session = test_util.create_mem_db(metadata, self.app.db)

        url = '/api/v1.0/activities'
        response = self.test_app.get(url)
        result = get_result(response)
        self.assertEqual(0, len(result))

    def test_get_activities(self):
        url = '/api/v1.0/activities'

        response = self.test_app.get(url)
        result = get_result(response)
        self.assertEqual(3, len(result))

    def test_get_activity(self):
        url = '/api/v1.0/activity/1'
        response = self.test_app.get(url)
        result = get_result(response)
        self.assertEqual('activity_0', result['name'])

    def test_get_tags(self):
        url = '/api/v1.0/tags'

        response = self.test_app.get(url)
        result = get_result(response)
        self.assertEqual(2, len(result))

    def test_get_tag(self):
        url = '/api/v1.0/tag/1'
        response = self.test_app.get(url)
        result = get_result(response)
        self.assertEqual('tag_0', result['tag'])

    def test_get_users(self):
        url = '/api/v1.0/tags'
        response = self.test_app.get(url)
        result = get_result(response)
        self.assertEqual(2, len(result))

    def test_get_user(self):
        url = '/api/v1.0/user/1'
        response = self.test_app.get(url)
        result = get_result(response)
        self.assertEqual('the_gigi', result['name'])
        self.assertEqual(1, result['role'])

    def test_add_user(self):
        url = '/api/v1.0/users'
        post_data = dict(name='spiderman',
                         email='peter.parker@dailybugle.com',
                         password='123')
        response = self.test_app.post(url, data=post_data)
        result = get_result(response)
        self.assertEqual('spiderman', result['name'])
        self.assertEqual(ROLE_USER, result['role'])

        # Try to get the same user
        id = result['id']

        q = self.session.query
        user = q(User).get(id)

        self.assertEqual(post_data['name'], user.name)
        self.assertEqual(post_data['email'], user.email)
        self.assertEqual(ROLE_USER, user.role)
        self.assertNotEqual(post_data['password'], user.password)  # hashed

    def _add_score(self, when, reps):
        if isinstance(when, datetime):
            when = when.date()

        q = self.session.query
        activity_id = q(Activity).first().id
        user_id = q(User).first().id
        url = '/api/v1.0/scores'
        comments = []
        tags = []

        post_data = dict(activity_id=activity_id,
                         user_id=user_id,
                         when=when,
                         reps=reps,
                         rx=True,
                         commets=comments,
                         tags=tags)
        response = self.test_app.post(url, data=post_data)
        self.assertEqual(200, response.status_code)

        return get_result(response)

    def test_add_score(self):
        """
        """
        when = datetime.now().date()
        self._add_score(when=when, reps=5)

        q = self.session.query
        score = q(Score).all()[-1]

        user_id = q(User).first().id

        self.assertEqual(user_id, score.user_id)
        self.assertEqual(when, score.when)
        self.assertEqual(5, score.reps)

    def test_get_score(self):
        when = datetime(2015, 1, 1)

        score_id1 = self._add_score(when, reps=3)['id']
        score_id2 = self._add_score(when + timedelta(days=1), reps=4)['id']
        url = '/api/v1.0/score'

        response = self.test_app.get('{}/{}'.format(url, score_id1))
        self.assertEqual(200, response.status_code)
        score1 = get_result(response)
        expected = dict(activity_id=1,
                        rx=True,
                        weight=None,
                        when='2015-01-01',
                        reps=3,
                        comments=None,
                        time=None,
                        tags=[],
                        score_type=dict(name=None, description=None),
                        id=7)
        self.assertEqual(expected, score1)

        response = self.test_app.get('{}/{}'.format(url, score_id2))
        self.assertEqual(200, response.status_code)
        score2 = get_result(response)
        expected = dict(activity_id=1,
                        rx=True,
                        weight=None,
                        when='2015-01-02',
                        reps=4,
                        comments=None,
                        time=None,
                        tags=[],
                        score_type=dict(name=None, description=None),
                        id=8)
        self.assertEqual(expected, score2)

    def test_get_scores(self):
        url = '/api/v1.0/scores'
        response = self.test_app.get(url)
        self.assertEqual(200, response.status_code)
        scores = get_result(response)
        self.assertEqual(6, len(scores))

    def test_update_score(self):
        q = self.session.query
        score = q(Score).first()
        self.assertEqual(1, len(score.tags))
        self.assertEqual('tag_0', score.tags[0].tag)

        self.assertNotEquals(666, score.reps)
        post_data = dict(tags='tag_1')
        url = '/api/v1.0/score/{}'.format(score.id)
        response = self.test_app.put(url, data=post_data)
        self.assertEqual(200, response.status_code)

        self.session.expire(score)
        self.session.refresh(score)

        score = q(Score).first()
        self.assertEqual(1, len(score.tags))
        self.assertEqual('tag_1', score.tags[0].tag)






