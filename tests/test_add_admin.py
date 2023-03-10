from flask_testing import TestCase
from app import create_app as app
from app import db
from app.models import User


class UserCreationTest(TestCase):

    def create_app(self):
        db.create_all()
        return app

    def test_create_user(self):
        user = User(username='test_user', password='test_password')
        db.session.add(user)
        db.session.commit()

        created_user = User.query.filter_by(username='test_user').first()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, 'test_user')
        self.assertEqual(created_user.password, 'test_password')
