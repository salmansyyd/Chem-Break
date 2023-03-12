from flask import Blueprint
from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required
from app.models import Apparatus, Breakage, Bank, Student, Record
from app.view_classes import ViewRecord
from app import db
import datetime

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return redirect(url_for('auth.login'))


@main.route('/home')
@login_required
def home():
    """
    List all modules.
    """
    return render_template('home.html')


@main.route('/home/breakage')
@login_required
def breakage():
    """
    Add / View Breakage records
    """
    apparatus_list = Apparatus.query.all()
    display_name_list = [apparatus.name + " " + apparatus.size
                         for apparatus in apparatus_list]
    print(display_name_list)
    return render_template('breakage.html', id_dname=zip(apparatus_list, display_name_list))


@main.route('/home/breakage', methods=['POST'])
@login_required
def post_breakage():
    """
    Add Breakage records
    """
    if request.method == 'POST':
        item = request.form['apparatus_id']
        quantity = request.form['quantity']
        roll_no = request.form['roll_no']
        s_class = request.form['class']
        section = request.form['section']
        total_ammount = int(quantity) * int(Apparatus.query.get(item).price)

        # check if student exists with roll_no and class
        student = Student.query.filter_by(roll_no=roll_no,
                                          class_=s_class).first()

        # if student does not exist, create a new student
        if student is None:
            student = create_student(roll_no, s_class, section)

        breakage = Breakage(item_id=item,
                            quantity=quantity, student_unique_id=student.unique_id, total_ammount=total_ammount)

        record_message = student.unique_id + " " + str(breakage.quantity) + " " + Apparatus.query.get(
            breakage.item_id).name + " " + Apparatus.query.get(breakage.item_id).size

        create_record(record_message, student.unique_id)

        create_bank(total_ammount, student.id, student.unique_id)

        db.session.add(breakage)
        db.session.commit()
    return redirect(url_for('main.breakage'))


def create_student(rollno, s_class, section):
    """
    Create a new student.
    """
    year = str(datetime.datetime.now().year)
    unique_id = str(s_class) + str(rollno) + "Y" + str(year[2:])

    student = Student(unique_id=unique_id, roll_no=rollno,
                      class_=s_class, section=section)

    db.session.add(student)
    db.session.commit()
    return student


def create_record(message, student_id):
    """
    Create a new record.
    """
    record = Record(
        message=message, student_unique_id=student_id)
    db.session.add(record)
    db.session.commit()
    return record


def create_bank(amount, student_id, unique_id):
    """
    Create a new bank record.
    """
    # check if unique_id exists
    bank = Bank.query.filter_by(unique_student_id=unique_id).first()
    if bank is not None:
        bank.amount = int(bank.amount) + int(amount)
        db.session.commit()
        return bank

    bank = Bank(amount=amount,
                unique_student_id=unique_id)
    db.session.add(bank)
    db.session.commit()
    return bank


@main.route('/home/report')
@login_required
def report():
    """
    Print report from a selected range of dates from a calendar.
    Possilbe inputs :
        class (fy, sy, ty)
        date (by default generate a months data.)
    """
    return "report"


@main.route("/home/records")
@login_required
def records():
    """
    List all records.
    Three subsections :
            1. Fy
            2. Sy
            3. Ty
    """
    return render_template('records.html')


@main.route('/home/help')
@login_required
def help():
    """
    Help page.
    """
    return render_template('help.html')


@main.route('/home/apparatus')
@login_required
def apparatus():
    """
    Add / Update / Delete apparatus.
    """
    return render_template('apparatus.html', apparatuses=Apparatus.query.all())


@main.route("/home/apparatus", methods=['POST'])
@login_required
def new_apparatus():
    """
    Add new apparatus.
    """
    if request.method == 'POST':
        name = request.form['name']
        size = request.form['size']
        price = request.form['price']
        apparatus = Apparatus(name=name, size=size, price=price)
        db.session.add(apparatus)
        db.session.commit()
    return redirect(url_for('main.apparatus'))


@main.route("/home/apparatus/<int:id>", methods=['GET', 'POST'])
@login_required
def update_apparatus(id):
    """
    Update apparatus.
    """

    if request.method == 'GET':
        return render_template('update_apparatus.html', apparatus=Apparatus.query.get(id))

    if request.method == 'POST':
        name = request.form['name']
        size = request.form['size']
        price = request.form['price']
        apparatus = Apparatus.query.get(id)
        apparatus.name = name
        apparatus.size = size
        apparatus.price = price
        db.session.commit()
    return redirect(url_for('main.apparatus'))


@main.route("/home/apparatus/<int:id>/delete", methods=['POST'])
@login_required
def delete_apparatus(id):
    """
    Delete apparatus.
    """
    if request.method == 'POST':
        apparatus = Apparatus.query.get(id)
        db.session.delete(apparatus)
        db.session.commit()
    return redirect(url_for('main.apparatus'))


@main.route("/home/records/<string:class_name>")
@login_required
def class_records(class_name):
    """
    List all records from a specific class.
    Three subsections :
        1. Fy
        2. Sy
        3. Ty
    """
    valid_classes = ['fy', 'sy', 'ty']
    if class_name.lower() not in valid_classes:
        abort(404)

    class_students = Student.query.filter_by(class_=class_name.lower()).all()
    class_records = []
    for student in class_students:
        item_id = Breakage.query.filter_by(
            student_unique_id=student.unique_id).first().item_id

        new_record = ViewRecord(
            date=Breakage.query.filter_by(
                student_unique_id=student.unique_id).first().date,
            roll_no=student.roll_no,
            class_=student.class_,
            section=student.section,
            apparatus=Apparatus.query.get(item_id).name,
            quantity=Breakage.query.filter_by(
                student_unique_id=student.unique_id).first().quantity,
            price=Apparatus.query.get(item_id).price,
            total_ammount=Breakage.query.filter_by(
                student_unique_id=student.unique_id).first().total_ammount,
        )

        class_records.append(new_record)

    return render_template('class_records.html', records=class_records, class_name=class_name.upper())
