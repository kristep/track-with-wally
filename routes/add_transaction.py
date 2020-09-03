import sqlite3
from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from helpers import login_required

from database import db
from models import Users
from models import Transactions
from models import Amounts

bp = Blueprint('add_transaction', __name__)


@bp.route('/add_income', methods=['GET', 'POST'])
@login_required
def add_income():
    if request.method == 'GET':
        return redirect(url_for('dashboard'))
    else:

        # Query database for current user balance
        balance = db.session.query(Users).filter_by(
            username=session["username"]).first().balance

        # get values from income form
        incAmount = float(request.form.get('inc_amount'))
        incTitle = request.form.get('inc_title')
        incDate = request.form.get('inc_date')

        # calculate balance
        # total_balance = round(float(balance) + float(incAmount), 2)
        total_balance = float("{:.2f}".format(
            float(balance) + float(incAmount)))

        # update balance in USERS table
        db.session.query(Users).filter_by(username=session["username"]).update(
            {Users.balance: total_balance}, synchronize_session=False)

        db.session.commit()

        # insert inc into TRANSACTION table
        income = Transactions(username=session["username"], title=incTitle,
                              inc_exp='inc', category='income', amount=incAmount, date=incDate)
        db.session.add(income)

        db.session.commit()

        flash("Income added")
        return redirect(url_for('dashboard.dashboard'))


@bp.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'GET':
        return redirect(url_for('dashboard'))
    else:
        # Query database for current user balance
        balance = db.session.query(Users).filter_by(
            username=session["username"]).first().balance

        # get values from expense form
        expAmount = float(request.form.get('exp_amount'))
        expTitle = request.form.get('exp_title')
        expDate = request.form.get('exp_date')
        expCategory = request.form.get('expense_category')

        # calculate total balance
        total_balance = round(float(balance) - float(expAmount), 2)

        # update balance in USERS table
        db.session.query(Users).filter_by(username=session["username"]).update(
            {Users.balance: total_balance}, synchronize_session=False)

        db.session.commit()

        # insert expense in TRANSACTIONS table
        expense = Transactions(username=session["username"], title=expTitle,
                               inc_exp='exp', category=expCategory, amount=expAmount, date=expDate)
        db.session.add(expense)

        db.session.commit()

        # calculate total expenses by category and add it to user AMOUNTS table
        expenses_categories = ('food', 'bills', 'transport', 'clothes',
                               'household', 'entertainment', 'holidays', 'other')

        for exp_item in expenses_categories:
            # if in AMOUNTS there is a row of concrete category -->
            if expCategory == exp_item:
                # select expenses amount from AMOUNTS
                if db.session.query(Amounts).filter_by(username=session["username"], category=exp_item).count() != 0:

                    exp_sum = db.session.query(Amounts).filter_by(
                        username=session["username"], category=exp_item).first().total

                    # calculate new expAmount
                    expAmount = round(
                        float(exp_sum) + float(expAmount), 2)
                    # and UPDATE AMOUNTS table
                    db.session.query(Amounts).filter_by(username=session["username"], category=exp_item).update(
                        {Amounts.total: expAmount}, synchronize_session=False)

                    db.session.commit()

                # else --> INSERT new row into AMOUNTS table
                else:
                    amount_row = Amounts(
                        username=session["username"], category=exp_item, total=expAmount)
                    db.session.add(amount_row)

                    db.session.commit()

        flash("Expense added")

        return redirect(url_for('dashboard.dashboard'))
