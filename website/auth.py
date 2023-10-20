from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .model import User


auth = Blueprint("auth", __name__)


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"), method="pbkdf2:sha256", salt_length=8)

        if name == "":
            flash("Name is empty.")
        elif email == "":
            flash("Email is empty.")
        elif password == "":
            flash("Password is empty.")
        else:
            new_user = User(
                name = name,
                email = email,
                password = password
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("view.home"))
    return render_template("register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email does not exist. Sign Up")
            return redirect(url_for("auth.login"))
        elif not check_password_hash(user.password, password):
            flash("Wrong password")
            return redirect(url_for("auth.login"))
        else:
            login_user(user)
            return redirect(url_for("view.home"))

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))