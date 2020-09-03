from database import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    hash = db.Column(db.String(256))
    balance = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Users name: {0}>'.format(self.username)


class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    title = db.Column(db.String(256))
    inc_exp = db.Column(db.String(32))
    category = db.Column(db.String(64))
    amount = db.Column(db.Float)
    date = db.Column(db.String(32))


class Amounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    category = db.Column(db.String(64))
    total = db.Column(db.Float)
