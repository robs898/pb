import yaml
import json
import requests
from pprint import pprint
import operator

cash=100

# get latest values from pb
with open("pb.yaml", 'r') as coins:
  try:
    y = yaml.load(coins)
  except yaml.YAMLError as exc:
    print(exc)
long_coins = y['coins']['long']
short_coins = y['coins']['short']

# get latest values from coinbase
call = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=150")
data = call.content
json = json.loads(data)

btc_price = float(json[0]['price_usd'])

# returns a list of coins that are below the pb values, various info is included as a dict
def populate(coins, distance):
  l = []
  for k, v in coins.iteritems():
    global json
    for c in json:
      if k == c['symbol']:
        price = float(c['price_usd'])
        if v > price:
          d = {}
          diff = abs(v - price)
          per_diff = (100* (diff / v))
          d['name'] = k
          d['up_to'] = v
          d['mkt_cap'] = float(c['market_cap_usd'])
          d['price'] = price
          d['diff'] = per_diff
          d['type'] = distance
          l.append(d)
  return l

longs = populate(long_coins, 'long')
shorts = populate(short_coins, 'short')

def calc_share(coins, cash):
  # calc total share
  a = []
  for coin in coins:
    a.append(coin['diff']) #* coin['mkt_cap'])

  tot_share = sum(a)
  
  # calc amount in btc and add to dict
  for coin in coins:
    coin['share'] = (coin['diff'] / tot_share) 
    coin['buy'] = (coin['share'] * cash)
    coin['buy_btc'] = (coin['buy'] / btc_price)

all_coins = longs + shorts
calc_share(all_coins, cash)
all_coins.sort(key=operator.itemgetter('diff'))
for coin in all_coins:
  if 'buy_btc' in coin:
    print coin['name'], coin['buy_btc']

