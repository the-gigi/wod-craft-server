import json
from unittest import TestCase

from api.api import create_app
from api.models import metadata, Activity
from tests.test_util import create_mem_db


class DataAPITest(TestCase):
    @classmethod
    def setUpClass(cls):
        # 1. Create in-memory test metadata DB
        cls.app = create_app()
        cls.session = create_mem_db(metadata, cls.app.db)
        cls.test_app = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.app.db.restore_engine()
        cls.test_app = None

    def setUp(self):
        """
        """
        # # Replace get_session() to make sure our test session is used.
        # # This is necessary because without it the metadata API gets
        # # a different memory session and the test can verify it.
        # self.original_get_session = sa_util.get_session
        #
        # sa_util.get_session = lambda x: self.session
        #
        # # Disable closing of the memory session to avoid wiping the database
        # self.session.close = lambda: None

    def tearDown(self):
        """
        """
        # sa_util.get_session = self.original_get_session

    def test_get_activities(self):
        url = '/api/v1.0/activities'
        response = self.test_app.get(url)
        result = json.loads(response.data)['result']
        self.assertEqual(0, len(result))

        # Add a few activities
        for i in range(3):
            a = Activity()
            a.name = 'activity_{}'.format(i)
            self.session.add(a)
        self.session.commit()

        response = self.test_app.get(url)
        result = json.loads(response.data)['result']
        self.assertEqual(3, len(result))


