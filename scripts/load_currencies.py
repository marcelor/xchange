from main import Currency, db
from money import CURRENCY

for code, obj in CURRENCY.items():
    currency = Currency(name=obj.name, iso_code=obj.code)
    db.session.add(currency)

db.session.commit()
