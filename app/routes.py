from flask import Blueprint, send_file, send_from_directory
from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required
from app.models import Apparatus, Breakage, Bank, Student, Record, User
from app.view_classes import ViewRecord, CollectMoney
from app import db
import datetime
import pytz
from sqlalchemy import and_

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return redirect(url_for('auth.login'))


@main.route('/admin/create', methods=['GET', 'POST'])
def create_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('create_account.html')


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
    Add records
    """
    apparatus_list = Apparatus.query.all()
    display_name_list = [apparatus.name + " " + apparatus.size
                         for apparatus in apparatus_list]
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
        date_ = request.form['date']
        total_ammount = int(quantity) * int(Apparatus.query.get(item).price)

        print(date_)
        # convert date to datetime
        date_obj = datetime.datetime.strptime(
            date_, "%Y-%m-%d").astimezone(pytz.utc)
        print(date_obj)
        print(datetime.datetime.utcnow())

        # check if student exists with roll_no and class
        student = Student.query.filter_by(roll_no=roll_no,
                                          class_=s_class).first()

        # if student does not exist, create a new student
        if student is None:
            student = create_student(roll_no, s_class, section)

        breakage = Breakage(item_id=item,
                            quantity=quantity, student_unique_id=student.unique_id, total_ammount=total_ammount, date=date_obj)

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
    return render_template('print_report.html')


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
        utc_date_str = str(Breakage.query.filter_by(
            student_unique_id=student.unique_id).first().date)
        utc_datetime = datetime.datetime.strptime(
            utc_date_str, "%Y-%m-%d %H:%M:%S.%f")
        date_str = utc_datetime.strftime("%d-%m-%Y")

        # only getting a single student record
        item_id = Breakage.query.filter_by(
            student_unique_id=student.unique_id).first().item_id

        new_record = ViewRecord(
            date=date_str,
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

    sorted_records = sorted(class_records, key=lambda x: x.roll_no)
    return render_template('class_records.html', records=sorted_records, class_name=class_name.upper())


@main.route("/test/home/records/<string:class_name>")
@login_required
def test_class_records(class_name):
    valid_classes = ['fy', 'sy', 'ty']
    if class_name.lower() not in valid_classes:
        abort(404)

    class_students = Student.query.filter_by(class_=class_name.lower()).all()
    view_records = []

    for student in class_students:
        breakages = Breakage.query.join(Apparatus).filter(
            and_(Breakage.student_unique_id == student.unique_id)).all()

        # loop through breakages and create view records
        for breakage in breakages:
            view_record = ViewRecord(
                date=breakage.date.strftime('%d/%m/%Y'),
                roll_no=student.roll_no,
                class_=student.class_,
                section=student.section,
                apparatus=breakage.apparatus.name + " " + breakage.apparatus.size,
                quantity=breakage.quantity,
                price=breakage.apparatus.price,
                total_ammount=breakage.quantity * breakage.apparatus.price
            )

            view_records.append(view_record)

    sorted_records = sorted(view_records, key=lambda x: x.roll_no)
    return render_template('class_records.html', records=sorted_records, class_name=class_name.upper())


@main.route("/home/records/getMoney/<string:class_name>")
@login_required
def getMoney(class_name):
    valid_classes = ['fy', 'sy', 'ty']
    if class_name.lower() not in valid_classes:
        abort(404)

    class_students = Student.query.filter_by(class_=class_name.lower()).all()
    class_records = []
    total_amount_to_collect = 0

    for student in class_students:
        bank = Bank.query.filter_by(
            unique_student_id=student.unique_id).first().amount
        total_amount_to_collect += bank
        collect_money = CollectMoney(
            rollno=student.roll_no,
            total_cash=bank,
        )
        class_records.append(collect_money)

    sorted_records = sorted(class_records, key=lambda x: x.rollno)
    return render_template('collect_money.html', collect_money_list=sorted_records, class_name=class_name.upper(), total_amount_to_collect=total_amount_to_collect)


@main.route("/home/reset_and_bakup")
@login_required
def reset_and_bakup():
    return render_template('reset_and_backup.html')


@main.route('/download_backup', methods=['POST'])
@login_required
def download_backup():
    return send_file('../app.db', as_attachment=True)


@main.route('/empty_user_table', methods=['POST'])
@login_required
def empty_user_table():
    db.session.query(User).delete()
    db.session.commit()

    return "User table has been emptied"


@main.route('/empty_breakage_table', methods=['POST'])
@login_required
def empty_breakage_table():
    db.session.query(Breakage).delete()
    db.session.commit()
    flash("Breakage table has been emptied", "success")
    return render_template('reset_and_backup.html')


@main.route('/empty_student_table', methods=['POST'])
@login_required
def empty_student_table():
    db.session.query(Student).delete()
    db.session.commit()
    flash("Student table has been emptied", "success")
    return render_template('reset_and_backup.html')


@main.route('/empty_apparatus_table', methods=['POST'])
@login_required
def empty_apparatus_table():
    db.session.query(Apparatus).delete()
    db.session.commit()
    flash("Apparatus table has been emptied", "success")
    return render_template('reset_and_backup.html')


@main.route('/empty_records_table', methods=['POST'])
@login_required
def empty_records_table():
    db.session.query(Record).delete()
    db.session.commit()
    flash("Records table has been emptied", "success")
    return render_template('reset_and_backup.html')


@main.route('/empty_bank_table', methods=['POST'])
@login_required
def empty_bank_table():
    db.session.query(Bank).delete()
    db.session.commit()
    flash("Bank table has been emptied", "success")
    return render_template('reset_and_backup.html')


@main.route('/complete_reset', methods=['POST'])
@login_required
def complete_reset():
    db.session.query(Breakage).delete()
    db.session.query(Student).delete()
    db.session.query(Record).delete()
    db.session.query(Bank).delete()
    db.session.commit()
    flash("All tables have been emptied", "success")
    return render_template('reset_and_backup.html')
