"""cryptospy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from coins.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('', main_page, name='index'),
    path('spy', spy_page, name='spy'),

    path('api_list', UserApiTemplateView.as_view(), name='api_list'),

    path('api_create', UserApiCreateView.as_view(), name='api_create'),


    path('api_update/<pk>', UserApiRequestUpdateView.as_view(), name='api_update'),

    path('api_delete/<pk>', UserApiRequestDeleteView.as_view(), name='api_delete'),


    path('register', register_page, name='register'),

    path('logged_out', logged_out_page, name='logged_out'),

    # path("password_reset", password_reset_request, name="password_reset"),

    path('accounts/', include('django.contrib.auth.urls')),

    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
    #name='password_reset_done'),

    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"),
    #name='password_reset_confirm'),

    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
    #name='password_reset_complete'),

    path('404.html', four_houndred_four_page, name='404'),

    path('create_wallet', UserWalletRequestCreateView.as_view(),  name='create_wallet'),

    path('wallet_lists', UserWalletRequestListView.as_view(), name='wallet_lists'),

    path('wallet_update/<pk>', UserWalletRequestUpdateView.as_view(), name='wallet_update'),

    path('wallet_delete/<pk>', UserWalletRequestDeleteView.as_view(), name='wallet_delete'),

    path('wallet_detail/<pk>', UserWalletRequestDetailView.as_view(), name='wallet_detail'),

    path('create_twitter_hashtag/<wallet_id>', TwitterHashTagsCreateView.as_view(), name='create_twitter_hashtag'),

    path('delete_twitter_hashtag/<pk>/<wallet_id>', TwitterHashTagsDeleteView.as_view(), name='delete_twitter_hashtag'),

    path('user_settings/<pk>', UserSettingsUpdateView.as_view(), name='user_settings'),

]

