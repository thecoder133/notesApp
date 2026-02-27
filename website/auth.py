from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged In!", category='success')
                login_user(user)
                return redirect(url_for('views.notes'))
            else:
                flash("Incorrect Password!", category='error')
        else:
            flash("No User Found! Sign Up First", category='error')
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/sign-up", methods=["POST", "GET"])
def signUp():
    if request.method == "POST":
        email = request.form["email"]
        first_name = request.form["firstName"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Account already exists!", category='error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters!", category="error")
        elif len(first_name) < 2:
            flash("Name must be greater than 1 character!", category="error")
        elif password1 != password2:
            flash("Passwords don't match!!", category="error")
        elif len(password1) < 7:
            flash("Password must be greater than 6 characters!", category="error")
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for('views.notes'))

    return render_template("signUp.html", user=current_user)

