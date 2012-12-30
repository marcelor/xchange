from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from local_settings import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    iso = db.Column(db.String(80), unique=True)

    def __init__(self, name, iso):
        self.name = name
        self.iso = iso

    def __repr__(self):
        return '<Currency %s>' % self.name


class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_currency_id = db.Column("Base currency", db.Integer, db.ForeignKey('currency.id'))
    currency_id = db.Column("Currency", db.Integer, db.ForeignKey('currency.id'))
    base_currency = db.relationship("Currency", primaryjoin="ExchangeRate.base_currency_id==Currency.id")
    currency = db.relationship("Currency", primaryjoin="ExchangeRate.currency_id==Currency.id")


@app.route("/")
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.run()
