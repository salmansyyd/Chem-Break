from app import db
from flask_login import UserMixin
from datetime import datetime


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
        item_id: item that broke (apparatus id)
        quantity: quantity of item that broke
        student_unique_id: student unique id
    """

    __tablename__ = "breakage"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    item_id = db.Column(db.Integer, db.ForeignKey(
        "apparatus.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    student_unique_id = db.Column(db.Integer, db.ForeignKey(
        "student.unique_id"), nullable=False)
    total_ammount = db.Column(db.Integer, nullable=False, default=0)
    student = db.relationship(
        'Student', backref='breakage', lazy=True)
    apparatus = db.relationship(
        'Apparatus', backref='breakage', lazy=True)

    def __repr__(self) -> str:
        return f"Breakage('{self.date}', '{self.item_id}', '{self.quantity}', '{self.student_unique_id}', '{self.total_ammount}')"

    def __init__(self, item_id, quantity, student_unique_id, total_ammount, date):
        self.item_id = item_id
        self.quantity = quantity
        self.student_unique_id = student_unique_id
        self.total_ammount = total_ammount
        self.date = date

    def get_dd_mm_yyyy(self):
        utc_datetime = datetime.datetime.strptime(
            self.date, "%Y-%m-%d %H:%M:%S.%f")
        date_str = utc_datetime.strftime("%d-%m-%Y")
        return date_str


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
    roll_no = db.Column(db.String(10), nullable=False)
    class_ = db.Column(db.String(10), nullable=False)
    section = db.Column(db.String(10), nullable=False, default="Chemistry")
    total_amount = db.relationship('Bank', backref='student', lazy=True)

    def __repr__(self) -> str:
        return f"Student('{self.unique_id}', '{self.roll_no}', '{self.class_}', '{self.section}')"

    def __init__(self, unique_id, roll_no, class_, section):
        self.unique_id = unique_id
        self.roll_no = roll_no
        self.class_ = class_
        self.section = section


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
    apparatus = db.relationship(
        'Breakage', backref='breakage', lazy=True, cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"Apparatus('{self.name}', '{self.size}', '{self.price}')"

    def __init__(self, name, size, price):
        self.name = name
        self.size = size
        self.price = price


class Record(db.Model):
    """
    Record Model
    parms:
        id: record id
        date: date of record
        message: message of record
        student_unique_id: student unique id
    """

    __tablename__ = "record"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.String(100), nullable=False)
    student_unique_id = db.Column(db.String(100), db.ForeignKey(
        "student.unique_id"), nullable=False)

    def __repr__(self) -> str:
        return f"Record('{self.date}', '{self.message}', '{self.student_unique_id}')"

    def __init__(self, message, student_unique_id):
        self.message = message
        self.student_unique_id = student_unique_id


class Bank(db.Model):
    """
    Bank Model
    parms:
        id: bank id
        amount: amount of money
        student_unique_id: student id
    """

    __tablename__ = "bank"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False, default=0)
    unique_student_id = db.Column(db.String(100), db.ForeignKey(
        "student.unique_id"),   nullable=False)

    def __repr__(self) -> str:
        return f"Bank('{self.amount}', '{self.unique_student_id})"

    def __init__(self, amount, unique_student_id):
        self.amount = amount
        self.unique_student_id = unique_student_id
