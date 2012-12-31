from decimal import Decimal
from lxml import etree
import requests
from StringIO import StringIO
from main import Currency, ExchangeRate, db

url = "http://www.brou.com.uy/web/guest/institucional/cotizaciones"

r = requests.get(url)
html = r.text
html = html.lower()

parser = etree.HTMLParser()
tree = etree.parse(StringIO(html), parser)

html = tree.getroot()

rate_table = html.xpath('//table')[1]

usd_rate_tr = rate_table.xpath('//tr')[1]

usd_buy_rate_td, usd_sell_rate_td = usd_rate_tr.xpath('//td')[4:6]

usd_buy_rate = usd_buy_rate_td.text
usd_sell_rate = usd_sell_rate_td.text

base_currency = Currency.query.filter_by(iso_code='UYU').first()
currency = Currency.query.filter_by(iso_code='USD').first()

rate = ExchangeRate()
rate.buy_rate = Decimal(usd_buy_rate)
rate.sell_rate = Decimal(usd_sell_rate)
rate.base_currency = base_currency
rate.currency = currency

db.session.add(rate)
db.session.commit()