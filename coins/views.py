import pprint

from django.shortcuts import render

# Create your views here.

# _*_ coding: utf-8 _*_
from django.http import HttpResponse


from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import logout as main_logout
from etherscan.stats import Stats
from .models import ApiStrings
from datetime import date, datetime

from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages


from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView

from .models import UserWalletRequest
from django import forms

from etherscan.accounts import Account
import time

import pprint
from decimal import Decimal
from .twitter import main


def main_page(request):
    key = ApiStrings.objects.filter(api_name="etherscan").first().api_string
    wallets = Wallet.objects.all()
    api = Stats(api_key=key)
    last_price = api.get_ether_last_price()
    eth_btc_time = last_price['ethbtc_timestamp']
    timestamp = datetime.fromtimestamp(int(eth_btc_time))
    return render(request, "coins/index.html", {"wallets": wallets, "last_price": last_price, "timestamp": timestamp})


@login_required(login_url='/login/')
def results_page(request):
    wallets = Wallet.objects.all()
    return render(request, "coins/userapistrings_list.html", {"wallets": wallets})


@login_required(login_url='/login/')
def spy_page(request):
    key = ApiStrings.objects.filter(api_name="etherscan").first().api_string
    wallets = Wallet.objects.all()
    api = Stats(api_key=key)
    last_price = api.get_ether_last_price()
    eth_btc_time = last_price['ethbtc_timestamp']
    timestamp = datetime.fromtimestamp(int(eth_btc_time))
    return render(request, "coins/spy.html", {"wallets": wallets, "last_price": last_price, "timestamp": timestamp})


def logged_out_page(request):
    wallets = Wallet.objects.all()
    logout(request)                                                                     # done?
    return render(request, "coins/logged_out.html", {"wallets": wallets})

"""
def logout(*args, **kwargs):
    resp = main_logout(*args, **kwargs)
    resp['Refresh'] = '3; /login/'      # redirects after 3 seconds to /account/login
    return resp
"""


def register_page(request):
    wallets = Wallet.objects.all()

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserSettings.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful.Thank You!")
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information. Try again!")
    form = NewUserForm()
    return render(request, "coins/register.html", {"wallets": wallets, "register_form": form})


# check
def homepage(request):
    return render(request=request, template_name="coins/index.html")


"""def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, '!!!!!! add @ here !!!!!!', [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found.')

                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("index")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html",
                  context={"password_reset_form": password_reset_form})
"""

def four_houndred_four_page(request):
    wallets = Wallet.objects.all()
    return render(request, "coins/404.html", {"wallets": wallets})


class UserWalletRequestCreateView(CreateView):
    model = UserWalletRequest
    fields = ["eth_adress", "label", "user", "minimum_income_to_spy", "maximum_income_to_spy", "api_key"]
    success_url = "spy"

    def get_initial(self):
        return {"user": self.request.user}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['user'].widget = forms.HiddenInput()
        form.fields['api_key'].queryset = UserApiStrings.objects.filter(user=self.request.user)
        return form


class UserWalletRequestListView(ListView):
    #model = UserWalletRequest

    def get_queryset(self):
        return UserWalletRequest.objects.filter(user=self.request.user)

    #template_name = "coins/userwalletrequest_list.html"

    #def get_context_data(self, **kwargs):
       # context = super().get_context_data(**kwargs)
       # context['user_wallet_list_all'] = UserWalletRequest.objects.filter(user=self.request.user)
        #return context


class UserWalletRequestUpdateView(UpdateView):
    model = UserWalletRequest
    fields = ["eth_adress", "label", "minimum_income_to_spy", "maximum_income_to_spy", "api_key"]
    success_url = reverse_lazy('wallet_lists')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['api_key'].queryset = UserApiStrings.objects.filter(user=self.request.user)
        return form


class UserWalletRequestDeleteView(DeleteView):
    model = UserWalletRequest
    success_url = reverse_lazy('wallet_lists')


class UserWalletRequestDetailView(DetailView):
    model = UserWalletRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_data'] = self.get_api_data()[0]
        context['balance'] = self.convert_balance(self.get_api_data()[1])
        context['twitter_hashtags'] = TwitterHashTags.objects.filter(user=self.request.user, wallet=self.object, mode="h")
        context['twitter_accounts'] = TwitterHashTags.objects.filter(user=self.request.user, wallet=self.object,
                                                             mode="u")
        context['twitter_data'] = main(self.request.user.settings.twitter_token)

        # pprint.pprint(context['api_data'][0])
        return context

    def convert_balance(self, balance):
        wei = Decimal(int(balance))
        power = 10 ** 18
        balance_converted = wei / power
        return balance_converted


    def get_api_data(self):
        api = Account(address=self.object.eth_adress, api_key=self.object.api_key.user_api_password)

        balance = api.get_balance()

        transactions = []
        for i in range(1):
            transactions += api.get_transaction_page(page=i, offset=1, sort='des')
            time.sleep(1)
        filtered_transactions = []

        for transaction in transactions:
            balance_converted = self.convert_balance(transaction['value'])
            if balance_converted >= self.object.minimum_income_to_spy and balance_converted <= self.object.maximum_income_to_spy:

                filtered_transactions.append({
                    'value': balance_converted,
                    'transaction_date': datetime.fromtimestamp(int(transaction['timeStamp'])),
                    'from': transaction['from'] if transaction['from'] != self.object.eth_adress else "",
                    'to': transaction['to'] if transaction['to'] != self.object.eth_adress else "",
                })
        return filtered_transactions, balance


class UserApiTemplateView(TemplateView):
    template_name = "coins/userapistrings_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_list_keys'] = UserApiStrings.objects.filter(user=self.request.user)
        return context


class UserApiCreateView(CreateView):
    model = UserApiStrings
    fields = ["user", "user_api_password", "user_api_name"]
    success_url = "api_list"

    def get_initial(self):
        return {"user": self.request.user}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['user'].widget = forms.HiddenInput()
        return form


class UserApiRequestUpdateView(UpdateView):
    model = UserApiStrings
    fields = ["user", "user_api_password", "user_api_name"]
    success_url = reverse_lazy('api_list')


class UserApiRequestDeleteView(DeleteView):
    model = UserApiStrings
    success_url = reverse_lazy('api_list')


class TwitterHashTagsCreateView(CreateView):
    model = TwitterHashTags
    fields = ["twitter_hash_tag", "user", "wallet", "twitter_username", "mode"]

    def get_success_url(self):
        return reverse_lazy('wallet_detail', args=[self.kwargs['wallet_id'], ])

    def get_initial(self):
        return {"user": self.request.user, "wallet": self.kwargs['wallet_id']}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['user'].widget = forms.HiddenInput()
        form.fields['wallet'].widget = forms.HiddenInput()
        return form


class TwitterHashTagsDeleteView(DeleteView):
    model = TwitterHashTags
    # success_url = reverse_lazy('wallet_detail')

    def get_success_url(self):
        return reverse_lazy('wallet_detail', args=[self.kwargs['wallet_id'], ])


class UserSettingsUpdateView(UpdateView):
    model = UserSettings
    fields = ["twitter_token"]
    success_url = reverse_lazy('spy')







# https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-editing/

# https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-display/

