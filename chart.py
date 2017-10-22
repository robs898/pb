import yaml
import json
import requests
from pprint import pprint
import operator
import pandas as pd
import sqlite3
import time

print('loading pb coins')
with open("pb.yaml", 'r') as coins:
  try:
    y = yaml.load(coins)
  except yaml.YAMLError as exc:
    print(exc)
long_coins = y['coins']['long']
short_coins = y['coins']['short']

print('getting latest values from cmc')
call = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=150")
data = call.content
json = json.loads(data)
btc_price = float(json[0]['price_usd'])

print('populating coins dict')
def populate(coins, distance):
  l = []
  for k, v in coins.iteritems():
    global json
    for c in json:
      if k == c['symbol']:
        price = float(c['price_usd'])
        d = {}
        d['symbol'] = k
        d['price'] = price
        #d['type'] = distance
        l.append(d)
  return l
longs = populate(long_coins, 'long')
shorts = populate(short_coins, 'short')
all_coins = longs + shorts

#print('creating dataframe')
#df = pd.DataFrame(all_coins)
#print (df)

print('creating db')
db = sqlite3.connect('coinsdb')
#db = sqlite3.connect(':memory:')
cursor = db.cursor()

print('creating tables')
l = []
for coin in all_coins:
    l.append(coin['symbol'] + ' TEXT')
coins = ', '.join(l)

#cursor.execute("CREATE TABLE coins(time TEXT PRIMARY KEY, %s)" % coins)
#db.commit()

#ce = db.execute('SELECT * FROM coins')
#names = list(map(lambda x: x[0], ce.description))
#print names

p = []
p.append(time.ctime())
for coin in all_coins:
    p.append(coin['price'])
cursor.execute("INSERT INTO coins VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", p)
db.commit()

cursor.execute('SELECT * FROM coins')
pprint(cursor.fetchall())

