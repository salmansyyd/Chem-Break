from flask import Blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required

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
    return "breakage"


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
    return "apparatus"
