from django.core.exceptions import ValidationError
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
    maximum_income_to_spy = models.CharField(max_length=10)
    twitter = models.BooleanField(default=False)
    mail = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.wallet.label}, {self.user.username}'


class UserWalletRequest(models.Model):
    eth_adress = models.CharField(max_length=42)
    label = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    minimum_income_to_spy = models.DecimalField(max_length=10, default=0.1, decimal_places=2, max_digits=20)
    maximum_income_to_spy = models.DecimalField(max_length=10, default=0.1, decimal_places=2, max_digits=20)
    twitter = models.BooleanField(default=False)
    mail = models.BooleanField(default=False)
    api_key = models.ForeignKey('UserApiStrings', on_delete=models.CASCADE, null=True)


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


class UserApiStrings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True)
    user_api_name = models.CharField(max_length=111)
    user_api_password = models.CharField(max_length=199, default="", blank=True)

    def __str__(self):
        # return self.api_string
        return f'{self.user_api_name}'


class TwitterHashTags(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    wallet = models.ForeignKey(UserWalletRequest, on_delete=models.CASCADE, null=True)
    twitter_hash_tag = models.CharField(max_length=42, default="", blank=True)
    twitter_username = models.CharField(max_length=42, default="", blank=True)
    mode = models.CharField(max_length=1, choices=(("h", "HASH TAG"), ("u", "ACCOUNT")), default="h")

    def clean(self):
        if self.mode == "h" and self.twitter_username:
                raise ValidationError("Mode HASHTAG, checked username. Try again")
        if self.mode == "u" and self.twitter_hash_tag:
                raise ValidationError("Mode USERNAME, checked hashtag. Try again")


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    twitter_token = models.CharField(max_length=150, blank=True, default="")



# python cryptospy/manage.py makemigrations
# python cryptospy/manage.py migrate



# Create your models here.
# on_delete=models.CASCADE - delete all settings if delete wallet
# on_delete=models.SET_NULL - if delete user,  user = none

# models.CharField - str
# models.TextField - str (more)
# models.DateTimeField - date, time
# models.ForeignKey - to another model
