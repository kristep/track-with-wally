import sqlite3
from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from sqlalchemy import asc, desc

from helpers import login_required
from database import db
from models import Users
from models import Transactions
from models import Amounts


bp = Blueprint('history', __name__, template_folder='../templates/history')


@bp.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    # get selections from url
    sel_show = request.args.get('show')
    sel_order = request.args.get('order')

    transactions = db.session.query(Transactions).filter_by(
        username=session["username"]).order_by(desc(Transactions.date)).all()

    # query database for transactions data by selected show value
    if sel_show == 'inc' or sel_show == 'exp':
        transactions = db.session.query(Transactions).filter_by(
            username=session["username"], inc_exp=sel_show).order_by(sel_order).all()
    elif sel_show == 'all':
        transactions = db.session.query(Transactions).filter_by(
            username=session["username"]).order_by(sel_order).all()

    return render_template("history.html", username=session["username"], transactions=transactions, sel_show=sel_show, sel_order=sel_order)


@bp.route('/select', methods=['GET', 'POST'])
@login_required
def select():

    if request.method == 'GET':
        return redirect(url_for('history'))
    else:
        # get selections from inputs
        sel_show = request.form.get(
            'sel_show') if request.form.get('sel_show') != "Select..." else 'all'
        sel_order = request.form.get('sel_order') if request.form.get(
            'sel_order') != "Select..." else 'date(desc)'

    return redirect(url_for('history.history', show=sel_show, order=sel_order))
