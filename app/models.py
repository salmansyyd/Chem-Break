from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """
    User Model for authentication
    parms:
        id: user id
        username: user name
        password: user password
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

    def check_password(self, password):
        return self.password == password


class Breakage(db.Model):
    pass


class Student(db.Model):
    pass


class Apparatus(db.Model):
    pass


class Record(db.Model):
    pass


class Bank(db.Model):
    pass
