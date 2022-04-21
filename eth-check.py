import sys
import requests
import math
import time


#brain={'eth-adress':['label', 'value', 'value_date', 'last_IN', 'last_OUT','spy_IN', 'spy=OUT']}
"""brain={'0xa1b1bbB8070Df2450810b8eB2425D543cfCeF79b':
           ['Come Back Alive UA',
            '297.212490028087598663',
            '2022-03-22',
            '2022-03-22',
            '2022-03-15',
            '0.5',
            '1']
       }

print(brain['0xa1b1bbB8070Df2450810b8eB2425D543cfCeF79b'])      # all about
print(brain['0xa1b1bbB8070Df2450810b8eB2425D543cfCeF79b'][0])   # label
print(brain['0xa1b1bbB8070Df2450810b8eB2425D543cfCeF79b'][1])   # value
print(brain['0xa1b1bbB8070Df2450810b8eB2425D543cfCeF79b'][2])   # date value
print(brain['0xa1b1bbB8070Df2450810b8eB2425D543cfCeF79b'][3])   # last IN
print(brain['0xa1b1bbB8070Df2450810b8eB2425D543cfCeF79b'][4])   # last OUT 
print(brain['0xa1b1bbB8070Df2450810b8eB2425D543cfCeF79b'][5])   # spy_IN
print(brain['0xa1b1bbB8070Df2450810b8eB2425D543cfCeF79b'][6])   # spy_OUT 
"""

print('Data from API:')

from etherscan.accounts import Account
import json
from decimal import Decimal
with open("stringone.txt", "r") as f:
    key = f.read().strip()

address = '0xa1b1bbB8070Df2450810b8eB2425D543cfCeF79b'          # sample wallet
api = Account(address=address, api_key=key)

# current
balance = api.get_balance()
print(balance)                  # 1 ether = 1000000000000000000 wei
# balance_converted = math.pow(10, -18) * int(balance)
# decimal
wei = Decimal(int(balance))
power = 10**18
balance_converted = wei/power
print(balance_converted)

# price eth/btc ; price eth/usd - index,spy

from etherscan.stats import Stats
api = Stats(api_key=key)
last_price = api.get_ether_last_price()
print(last_price)
print('ETH/BTC:', last_price['ethbtc'])
print('ETH/USD:', last_price['ethusd'])



eth_btc_time = last_price['ethbtc_timestamp']
print(eth_btc_time)   # w sekundach
eth_usd_time = last_price['ethusd_timestamp']
print(eth_btc_time)   # w sekundach


from datetime import date, datetime
int_eth_btc_time = int(eth_btc_time)
timestamp = datetime.fromtimestamp(int_eth_btc_time)
print("Data po konwersji to =", timestamp)


# sys.exit()



# transactions 1 - bugs
"""from etherscan.accounts import Account
address = '0xa1b1bbB8070Df2450810b8eB2425D543cfCeF79b'
api = Account(address=address, api_key=key)
transactions = api.get_all_transactions(offset=3, sort='asc', internal=False)
print(transactions[0])"""

# transactions 2 - ok
from etherscan.accounts import Account
address = '0xa1b1bbB8070Df2450810b8eB2425D543cfCeF79b'      # sample wallet
api = Account(address=address, api_key=key)

transactions = []

for i in range(1):
    transactions += api.get_transaction_page(page=i, offset=1, sort='des')
    print(transactions)
    time.sleep(1)


for i in transactions:
    print('value:', i["value"])
address = '0x49edf201c1e139282643d5e7c6fb0c7219ad1db7'

