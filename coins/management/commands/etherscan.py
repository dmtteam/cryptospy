# https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/

from django.core.management.base import BaseCommand, CommandError
from coins.models import Wallet, WalletHistory
from coins.tools import EtherscanApi



class Command(BaseCommand):
    help = 'Closes the specified poll for voting'


    def handle(self, *args, **options):
        print('ok')
        # repetitive operations
        for wallet in Wallet.objects.all():
            print(wallet)
            etherscanapi=EtherscanApi(wallet.eth_adress)
            transactions=etherscanapi.get_transactions()

            # print(transactions)
            for transaction in transactions:
                try:
                    history=WalletHistory.objects.get_or_create(wallet=wallet, hash=transaction["hash"])
                    history.value=transaction["value"]
                    history.timestamp = transaction["timeStamp"]
                    history.save()
                except AttributeError:
                    print(transaction)
                break