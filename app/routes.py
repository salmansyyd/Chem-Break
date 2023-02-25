from flask import Blueprint
from flask import render_template

main = Blueprint('main', __name__)


@main.route('/home')
def home():
    return render_template('home.html')
