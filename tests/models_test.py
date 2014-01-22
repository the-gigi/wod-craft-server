from unittest import TestCase
from api import models
from api.models import User
from tests.test_util import create_mem_db


class ModelsTest(TestCase):
    def setUp(self):
        self.db = create_mem_db(models.db.metadata)

    def tearDown(self):
        pass

    def test_user(self):
        q = self.db.query
        self.assertEqual(0, q(User).count())

        user = User()
        user.email = 'user@tempuri.org'
        user.nickname = 'hercules'

        self.db.add(user)
        self.db.commit()

        self.assertEqual(1, q(User).count())
        u = q(User).one()

        self.assertEqual(u.email, user.email)
        self.assertEqual(u.nickname, user.nickname)
