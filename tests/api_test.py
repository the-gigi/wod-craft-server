import json
from unittest import TestCase

from api.api import create_app
from api.models import (
    metadata,
    Activity,
    Score,
    Tag,
    User,
    ROLE_USER,
    ROLE_ADMIN)

from tests.test_util import create_mem_db


class APITest(TestCase):
    def setUp(self):
        """
        """
        # Create in-memory test metadata DB
        self.app = create_app()
        self.session = create_mem_db(metadata, self.app.db)
        self.test_app = self.app.test_client()

        # Add admin and regular users
        user = User()
        user.nickname = 'the_gigi'
        user.email = 'the_gigi@gmail.com'
        user.role = ROLE_ADMIN
        self.session.add(user)

        user2 = User()
        user2.nickname = 'nobody'
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
        self.session = create_mem_db(metadata, self.app.db)

        url = '/api/v1.0/activities'
        response = self.test_app.get(url)
        result = json.loads(response.data)['result']
        self.assertEqual(0, len(result))

    def test_get_activities(self):
        url = '/api/v1.0/activities'

        response = self.test_app.get(url)
        result = json.loads(response.data)['result']
        self.assertEqual(3, len(result))

    def test_get_activity(self):
        url = '/api/v1.0/activity/1'
        response = self.test_app.get(url)
        result = json.loads(response.data)['result']
        self.assertEqual('activity_0', result['name'])

    def test_get_tags(self):
        url = '/api/v1.0/tags'

        response = self.test_app.get(url)
        result = json.loads(response.data)['result']
        self.assertEqual(2, len(result))

    def test_get_tag(self):
        url = '/api/v1.0/tag/1'
        response = self.test_app.get(url)
        result = json.loads(response.data)['result']
        self.assertEqual('tag_0', result['tag'])

    def test_get_users(self):
        url = '/api/v1.0/tags'
        response = self.test_app.get(url)
        result = json.loads(response.data)['result']
        self.assertEqual(2, len(result))

    def test_get_user(self):
        url = '/api/v1.0/user/1'
        response = self.test_app.get(url)
        result = json.loads(response.data)['result']
        self.assertEqual('the_gigi', result['nickname'])
        self.assertEqual(1, result['role'])


