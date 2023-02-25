from . import auth
from flask import render_template, redirect, url_for, request, flash
from flask import request
from app.models import User


@auth.route("/login")
def login():
    return render_template("auth/login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(username=username).first()

    if username != "salman" and password != "salman":
        flash("Invalid Credentials!")
        return redirect(url_for("auth.login"))

    # if not user or not user.check_password(password):
    #     flash("Please check your login details and try again.")
    #     return redirect(url_for("auth.login"))

    return redirect(url_for("main.home"))


@auth.route("/logout")
def logout():
    return render_template("auth/login.html")
