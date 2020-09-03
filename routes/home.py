from flask import render_template, Blueprint


bp = Blueprint('home', __name__, template_folder='../templates/home')


@bp.route('/')
def home():
    return render_template("home.html")
