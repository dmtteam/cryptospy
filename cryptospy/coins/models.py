from django.db import models
from django.contrib.auth.models import User
from django import forms


class Wallet(models.Model):
    eth_adress = models.CharField(max_length=42)
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


class UserWallet(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    minimum_income_to_spy = models.CharField(max_length=10)
    minimum_outcome_to_spy = models.CharField(max_length=10)
    twitter = models.BooleanField(default=False)
    mail = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.wallet.label}, {self.user.username}'

class UserWalletRequest(models.Model):
    eth_adress = models.CharField(max_length=42)
    label = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    minimum_income_to_spy = models.CharField(max_length=10)
    minimum_outcome_to_spy = models.CharField(max_length=10)
    twitter = models.BooleanField(default=False)
    mail = models.BooleanField(default=False)


class WalletHistory(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True)
    timestamp = models.IntegerField(null=True)
    hash = models.CharField(max_length=150)
    value = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.wallet.label}, {self.timestamp}'    # check here


class ApiStrings(models.Model):
    api_name = models.CharField(max_length=111)
    api_string = models.CharField(max_length=199)
    password = models.CharField(max_length=199, default="", blank=True)

    def __str__(self):
        # return self.api_string
        return f'{self.api_name}'

    def save(self, *args, **kwargs):
        if self.password:
            self.api_string = self.password
            self.password = ""
        super().save(*args, **kwargs)


# python cryptospy/manage.py makemigrations
# python cryptospy/manage.py migrate



# Create your models here.
# on_delete=models.CASCADE - delete all settings if delete wallet
# on_delete=models.SET_NULL - if delete user,  user = none

# models.CharField - str
# models.TextField - str (more)
# models.DateTimeField - date, time
# models.ForeignKey - to another model
