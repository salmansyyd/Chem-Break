from flask_testing import TestCase
from app import create_app as app_factory
from app import db
from app.models import User
import unittest
from config import Testing as Config

NEW_USERNAME = "salman"
NEW_PASSWORD = "salman"


class UserCreationTest(TestCase):

    def create_app(self):
        app = app_factory(config=Config)
        return app

    def setUp(self):
        db.create_all()

    def test_create_user(self):
        user = User(username=NEW_USERNAME, password=NEW_PASSWORD)
        db.session.add(user)
        # db.session.commit()

        created_user = User.query.filter_by(username=NEW_USERNAME).first()
        print(created_user)
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, NEW_USERNAME)
        self.assertEqual(created_user.password, NEW_PASSWORD)

    def tear_down(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
