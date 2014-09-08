from unittest import TestCase
from api import models
from api.models import User
from tests.test_util import create_mem_db


class ModelsTest(TestCase):
    def setUp(self):
        self.session = create_mem_db(models.metadata, models.db)

    def tearDown(self):
        # See documentation for create_mem_db()
        models.db.restore_engine()

    def test_user(self):
        q = self.session.query
        self.assertEqual(0, q(User).count())

        user = User()
        user.email = 'user@tempuri.org'
        user.nickname = 'hercules'

        self.session.add(user)
        self.session.commit()

        self.assertEqual(1, q(User).count())
        u = q(User).one()

        self.assertEqual(u.email, user.email)
        self.assertEqual(u.nickname, user.nickname)


