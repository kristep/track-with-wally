import sqlite3
from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import DataRequired
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

import ctypes


from models import Users
from models import Transactions
from models import Amounts
from database import db


bp = Blueprint('auth', __name__, template_folder='../templates/auth')


@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        error = None

        user = db.session.query(Users).filter_by(
            username=request.form.get("username")).one_or_none()

        if user and check_password_hash(user.hash, request.form.get("password")):
            session["user_id"] = user.id
            session["username"] = user.username

            # Redirect user to dashboard
            return redirect(url_for("dashboard.dashboard", user_id=session["user_id"], username=session["username"]))
        else:
            error = "invalid username and/or password"
            return render_template("login.html", error=error)


# Register Form Class
class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        # from form get username, get and hash password
        username = form.username.data
        password = generate_password_hash(form.password.data)

        user = Users(username=username, hash=password)
        db.session.add(user)
        db.session.commit()

        flash("You are successfully registered.")
        return redirect(url_for('home.home'))

    return render_template("register.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    # Forget user_id and redirect to homepage
    session.clear()
    flash("You are logged out. See You next time!")
    return redirect(url_for('home.home'))


# account settings Form Class
class PasswordForm(Form):
    curr_password = PasswordField('Current Password')
    new_password = PasswordField('New Password', [
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


class UsernameForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=25)])
    new_username = StringField(
        'New Username', [validators.Length(min=3, max=25)])


@bp.route('/change_username', methods=["GET", "POST"])
@login_required
def change_username():
    usn_form = UsernameForm(request.form)

    if request.method == 'POST' and usn_form.validate():
        # from form get data
        username = usn_form.username.data
        new_username = usn_form.new_username.data

        # check if username is current logged user, and change username in db
        if username == session['username']:
            # update username in USERS, TRANSACTIONS and AMOUNTS tables
            db.session.query(Users).filter_by(username=session["username"]).update(
                {Users.username: new_username}, synchronize_session=False)

            db.session.query(Transactions).filter_by(username=session["username"]).update(
                {Transactions.username: new_username}, synchronize_session=False)

            db.session.query(Amounts).filter_by(username=session["username"]).update(
                {Amounts.username: new_username}, synchronize_session=False)

            db.session.commit()

            session["username"] = new_username

            flash("username changed")
            return redirect(url_for('dashboard.dashboard'))

    return render_template('/change_username.html', usn_form=usn_form)


@bp.route('/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    psw_form = PasswordForm(request.form)

    if request.method == 'POST' and psw_form.validate():

        curr_password = psw_form.curr_password.data
        new_password = generate_password_hash(psw_form.new_password.data)
        confirm = psw_form.confirm.data

        # check if current password is correct (in db)
        passw = db.session.query(Users).filter_by(
            username=session["username"]).first().hash

        if check_password_hash(passw, curr_password):
            # update password in USERS tables
            db.session.query(Users).filter_by(username=session["username"]).update(
                {Users.hash: new_password}, synchronize_session=False)

            db.session.commit()

            flash("Password changed.")
            return redirect(url_for('dashboard.dashboard'))

        else:
            flash("Current password is not correct.")
            return redirect(url_for('auth.change_password'))
    return render_template('/change_password.html', psw_form=psw_form)


@bp.route('/clear_all', methods=["GET", "POST"])
@login_required
def clear_all():

    # make alert box, for user to confirm deletion
    ctypes.windll.user32.MessageBoxW(
        0, "Are you shure you want to delete all data?", "Your title", 1)

    # delete all data from transactions, amounts and balance from users
    db.session.query(Transactions).filter_by(
        username=session["username"]).delete()
    db.session.query(Amounts).filter_by(username=session["username"]).delete()
    db.session.query(Users).filter_by(username=session["username"]).update(
        {Users.balance: 0}, synchronize_session=False)
    db.session.commit()

    return redirect(url_for("dashboard.dashboard"))
