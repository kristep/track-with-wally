import os

from flask import Flask, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from database import db


from routes.auth import bp as auth_bp
from routes.add_transaction import bp as add_transaction_bp
from routes.dashboard import bp as dashboard_bp
from routes.statistics import bp as statistics_bp
from routes.history import bp as history_bp
from routes.home import bp as home_bp


from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp)
    app.register_blueprint(add_transaction_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(home_bp)

    app.secret_key = b'_5#y2L"G4O0z\n\xec]/'

    app.config.from_object(os.getenv('FLASK_CONFIG', 'config.DevConfig'))

    db.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
