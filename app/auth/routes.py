from . import auth
from flask import render_template, redirect, url_for, request, flash
from flask import request
from app.models import User
from flask_login import login_user, logout_user, login_required


@auth.route("/login")
def login():
    return render_template("auth/login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)

    return redirect(url_for("main.home"))


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
