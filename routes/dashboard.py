import sqlite3
from helpers import login_required

from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from flask_session import Session

from database import db
from models import Users
from models import Transactions
from models import Amounts
from sqlalchemy import desc
bp = Blueprint('dashboard', __name__, template_folder='../templates/dashboard')


@bp.route('/dashboard')
@login_required
def dashboard():
    error = ''

    balance = db.session.query(Users).filter_by(
        username=session["username"]).first().balance

    if balance < 0:
        error = "your balance is negative!"

    # query database for transactions data
    transactions = db.session.query(Transactions).filter_by(
        username=session["username"]).order_by(desc(Transactions.date)).limit(10).all()

    # make expenses dictionary (and pass it to dashboard.html), where keys dynamically will be expenses categories (same as radio input values)
    expenses_categories = ('food', 'bills', 'transport',
                           'clothes', 'household', 'entertainment', 'holidays', 'other')

    expenses = {}
    for exp_item in expenses_categories:
        expenses[exp_item] = db.session.query(Amounts).filter_by(username=session["username"], category=exp_item).first(
        ).total if db.session.query(Amounts).filter_by(username=session["username"], category=exp_item).count() > 0 else 0.00

    return render_template("dashboard.html", username=session["username"], balance=balance, expenses=expenses, transactions=transactions, error=error)


@bp.route('/delete/<string:id>', methods=['POST'])
@login_required
def delete(id):
    # update total balance in USERS
    # Query database for current user balance
    balance = db.session.query(Users).filter_by(
        username=session["username"]).first().balance

    # get transaction amount from TRANSACTIONS
    expAmount = db.session.query(Transactions).filter_by(
        username=session["username"], id=id).first().amount

    # get category from TRANSACTIONS
    category = db.session.query(Transactions).filter_by(
        username=session["username"], id=id).first().category

    # calculate total balance
    total_balance = round(float(balance) - float(expAmount),
                          2) if category == 'income' else round(float(balance) + float(expAmount), 2)

    # update balance in USERS table
    db.session.query(Users).filter_by(username=session["username"]).update(
        {Users.balance: total_balance}, synchronize_session=False)

    db.session.commit()

    # update/delete AMOUNTS (just for expenses)
    if category != 'income':
        # select expenses amount from AMOUNTS
        exp_sum = db.session.query(Amounts).filter_by(
            username=session["username"], category=category).first().total

        expAmount = round(float(exp_sum) - float(expAmount), 2)

        db.session.query(Amounts).filter_by(username=session["username"], category=category).update(
            {Amounts.total: expAmount}, synchronize_session=False)

        db.session.commit()

    # delete transaction from TRANSACTIONS table
    db.session.query(Transactions).filter_by(id=id).delete()

    db.session.commit()

    flash("Successfully deleted")
    return redirect(url_for('dashboard.dashboard'))
