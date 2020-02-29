from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from paperclip.models import User
from paperclip.extensions import db
from paperclip.routes import main

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_address = request.form.get("email_address")
        password = request.form.get("password")
        remember_me = True if request.form.get("remember_me") == "on" else False

        user = User.query.filter_by(email_address=email_address).first()

        if not user or not check_password_hash(user.password_hash, password):
            return redirect(url_for("auth.login"))

        login_user(user, remember=remember_me)
        return redirect(url_for("main.index"))

    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    error_message = ""

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email_address = request.form.get("email_address")
        password = request.form.get("password")
        password_repeat = request.form.get("password_repeat")

        user = User.query.filter_by(email_address=email_address).first()

        if not user:
            user = User(
                user_name=first_name + " " + last_name,
                email_address=email_address,
                password=password,
            )

            db.session.add(user)
            db.session.commit()

            return redirect(url_for("auth.login"))

        else:
            error_message = "User with this email address already exists, please log in"

    return render_template("register.html", error_message=error_message)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
