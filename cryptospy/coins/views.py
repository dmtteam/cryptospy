from django.shortcuts import render

# Create your views here.

# _*_ coding: utf-8 _*_
from django.http import HttpResponse


from django.shortcuts import render
from .models import Wallet
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

from django.views.generic.edit import CreateView
from django.views.generic import ListView

from .models import UserWalletRequest
from django import forms

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
    return render(request, "coins/results.html", {"wallets": wallets})


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
                        send_mail(subject, email, 'cryptospyalert@gmail.com', [user.email], fail_silently=False)
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
    fields = ["eth_adress", "label", "user", "minimum_income_to_spy", "minimum_outcome_to_spy", "twitter", "mail"]
    success_url = "spy"

    def get_initial(self):
        return {"user": self.request.user}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['user'].widget = forms.HiddenInput()
        return form


class UserWalletRequestListView(ListView):
    model = UserWalletRequest


#update view
#delete view
#detail view




