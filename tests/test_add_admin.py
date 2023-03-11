from flask_testing import TestCase
from app import create_app as app_factory
from app import db
from app.models import User
import unittest
from config import Config

NEW_USERNAME = "salman"
NEW_PASSWORD = "salman"


class UserCreationTest(TestCase):

    def create_app(self):
        app = app_factory(config=Config)
        db.create_all()
        return app

    def test_create_user(self):
        user = User(username=NEW_USERNAME, password=NEW_PASSWORD)
        db.session.add(user)
        db.session.commit()

        created_user = User.query.filter_by(username='test_user').first()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, 'test_user')
        self.assertEqual(created_user.password, 'test_password')


if __name__ == "__main__":
    unittest.main()
