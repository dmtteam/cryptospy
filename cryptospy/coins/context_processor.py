from .models import ApiStrings
from etherscan.stats import Stats
from .models import Wallet
from datetime import date, datetime


def subject_renderer(request):
    key = ApiStrings.objects.filter(api_name="etherscan").first().api_string
    wallets = Wallet.objects.all()
    api = Stats(api_key=key)
    last_price = api.get_ether_last_price()
    eth_btc_time = last_price['ethbtc_timestamp']
    timestamp = datetime.fromtimestamp(int(eth_btc_time))
    return {"wallets": wallets, "last_price": last_price, "timestamp": timestamp}

# https://betterprogramming.pub/django-quick-tips-context-processors-da74f887f1fc

