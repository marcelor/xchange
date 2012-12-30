from main import Currency, db
from money import CURRENCY

for code, obj in CURRENCY.items():
    currency = Currency(obj.name, obj.code)
    db.session.add(currency)

db.session.commit()
