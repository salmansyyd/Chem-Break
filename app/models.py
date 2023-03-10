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

    """
    Breakage Model
    parms:
        id: breakage id
        date: date of breakage
        item: item that broke (apparatus id)
        quantity: quantity of item that broke
        student_id: student id
    """

    __tablename__ = "breakage"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    student_unique_id = db.Column(db.Integer, db.ForeignKey(
        "student.unique_id"), nullable=False)


class Student(db.Model):
    """
    Student Model
    parms:
        id: student id
        unique_id: student unique id
        roll_no: student roll number
        class: student class (fy, sy, ty)
        section: department section (Chemistry)
    """

    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(100), unique=True, nullable=False)
    roll_no = db.Column(db.String(10), unique=True, nullable=False)
    class_ = db.Column(db.String(10), nullable=False)
    section = db.Column(db.String(10), nullable=False, default="Chemistry")
    total_amount = db.relationship('Bank', backref='student', lazy=True)


class Apparatus(db.Model):
    """
    Apparatus Model
    parms:
        id: apparatus id
        name: apparatus name
        size: apparatus size
        price: apparatus price
    """

    __tablename__ = "apparatus"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)


class Record(db.Model):
    """
    Record Model
    parms:
        id: record id
        date: date of record
        message: message of record
        student_id: student id
    """

    __tablename__ = "record"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(100), nullable=False)
    student_unique_id = db.Column(db.String(100), db.ForeignKey(
        "student.unique_id"), nullable=False)


class Bank(db.Model):
    """
    Bank Model
    parms:
        id: bank id
        student_unique_id: student id
        amount: amount of money
    """

    __tablename__ = "bank"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False, default=0)
    unique_student_id = db.Column(db.String(100), db.ForeignKey(
        "student.unique_id"),   nullable=False)
