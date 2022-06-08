from django.contrib import admin
from .models import Wallet, UserWallet, WalletHistory, ApiStrings


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    pass


@admin.register(WalletHistory)
class WalletHistoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ApiStrings)
class WalletHistoryAdmin(admin.ModelAdmin):
    fields = ["api_name", "password"]

# Register your models here.
