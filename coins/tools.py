import sys
import requests
import math
import time
import json
import os
from decimal import Decimal
from etherscan.accounts import Account
from etherscan.stats import Stats
from datetime import date, datetime
from .models import ApiStrings


class EtherscanApi:
    def __init__(self, address):
        self.key = ApiStrings.objects.filter(api_name="etherscan").first().api_string
        self.address = address
        self.api = Account(address=self.address, api_key=self.key)

    def get_transactions(self):
        transactions = []
        for i in range(3):
            transactions += self.api.get_transaction_page(page=i, offset=1, sort='des')
            # print(transactions)
            time.sleep(1)
        return transactions

    # get_transactions()


    def get_last_price(self):
        self.api = Stats(api_key=self.key)
        last_price = self.api.get_ether_last_price()
        print(last_price)
        print('ETH/BTC:', last_price['ethbtc'])
        print('ETH/USD:', last_price['ethusd'])

        eth_btc_time = last_price['ethbtc_timestamp']
        print(eth_btc_time)  # w sekundach
        eth_usd_time = last_price['ethusd_timestamp']
        print(eth_btc_time)  # w sekundach

        int_eth_btc_time = int(eth_btc_time)
        timestamp = datetime.fromtimestamp(int_eth_btc_time)

        #return last_price['ethbtc'], \
        #last_price['ethusd'], \
        #last_price['ethbtc_timestamp'], \
        #last_price['ethusd_timestamp']

        get_last_price()

    def get_balance(self):
        balance = self.api.get_balance()
        print(balance)                                                   # 1 ether = 1000000000000000000 wei
        # decimal
        wei = Decimal(int(balance))
        power = 10 ** 18
        balance_converted = wei / power
        print(balance_converted)

    # get_balance()







"""for i in transactions:
    print('wartosci transakcji to:', i["value"])"""

