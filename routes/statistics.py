import sqlite3
import pygal
from pygal.style import Style
from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from helpers import login_required

from database import db
from models import Users
from models import Transactions
from models import Amounts

bp = Blueprint('statistics', __name__,
               template_folder='../templates/statistics')

custom_style = Style(
    background='transparent',
    opacity='.7',
    opacity_hover='1',
    transition='400ms ease-in',
    colors=('#F28A80', '#F2AF88', '#F2E49B', '#c9e49e', '#30bb59', '#72d6d6', '#327ba8', '#bd89d4'))


@bp.route("/statistics")
@login_required
def statistics():
    # connect to db
    expenses_categories = ('food', 'bills', 'transport',
                           'clothes', 'household', 'entertainment', 'holidays', 'other')

    expenses = {}
    for exp_item in expenses_categories:
        expenses[exp_item] = db.session.query(Amounts).filter_by(username=session["username"], category=exp_item).first(
        ).total if db.session.query(Amounts).filter_by(username=session["username"], category=exp_item).first() else 0.00

    # make expenses graph and return
    line_chart = pygal.HorizontalBar(style=custom_style)
    line_chart.title = 'Expenses total amounts by categories (EUR)'
    for key, value in expenses.items():
        line_chart.add(key, value)
    chart = line_chart.render_data_uri()

    return render_template("statistics.html", chart=chart, username=session["username"])
