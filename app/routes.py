from flask import Blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.models import Apparatus
from app import db

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
    return render_template('breakage.html')


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
    return redirect(url_for('main.apparatus', apparatuses=Apparatus.query.all()))
