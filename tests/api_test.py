import json
from unittest import TestCase

from api.api import create_app
from api.models import metadata, Activity, Score
from tests.test_util import create_mem_db


class DataAPITest(TestCase):
    def setUp(self):
        """
        """
        # 1. Create in-memory test metadata DB
        self.app = create_app()
        self.session = create_mem_db(metadata, self.app.db)
        self.test_app = self.app.test_client()

        # 2. Add a few activities
        activities = []
        for i in range(3):
            a = Activity()
            a.name = 'activity_{}'.format(i)
            activities.append(a)
            self.session.add(a)

        # 3. Add a few scores
        for i in range(3):
            for j in range(2):
                s = Score()
                s.activity = activities[i]
                s.rx = j == 0
                s.reps = j

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


