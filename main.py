from decimal import Decimal
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
from local_settings import SQLALCHEMY_DATABASE_URI, DEBUG_MODE

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


class Currency(db.Model):
    """ISO alpha-3"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    iso_code = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return '<Currency %s>' % self.name


class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_currency_id = db.Column("Base currency", db.Integer, db.ForeignKey('currency.id'))
    currency_id = db.Column("Currency", db.Integer, db.ForeignKey('currency.id'))
    base_currency = db.relationship("Currency", backref='base currencies', primaryjoin="ExchangeRate.base_currency_id==Currency.id")
    currency = db.relationship("Currency", backref='currencies', primaryjoin="ExchangeRate.currency_id==Currency.id")
    buy_rate = db.Column("Buy rate", db.Float, default=Decimal('0'))
    sell_rate = db.Column("Sell rate", db.Float, default=Decimal('0'))

    def __repr__(self):
        return '<Exchange rate: %s ---> %s>' % (self.base_currency.iso_code, self.currency.iso_code)

# Create the database tables.
db.create_all()

@app.route("/")
def index():
    base_currency = Currency.query.filter_by(iso_code='UYU').first()
    currency = Currency.query.filter_by(iso_code='USD').first()
    rate = ExchangeRate.query.filter_by(base_currency=base_currency, currency=currency).first()
    return render_template('home.html', buy_rate=rate.buy_rate, sell_rate=rate.sell_rate)


# Create the Flask-Restless API manager.
manager = APIManager(app, flask_sqlalchemy_db=db)
# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(ExchangeRate, methods=['GET'], include_columns=['base_currency', 'base_currency.name', 'base_currency.iso_code', \
    'currency', 'currency.name', 'currency.iso_code', \
    'buy_rate', 'sell_rate'], \
    collection_name='rates')


if __name__ == '__main__':
    app.debug = DEBUG_MODE
    app.run()
