"""
URL mappings for the Coin API.
"""
from django.urls import path

from coin import views

app_name = 'coin'

urlpatterns = [
    path('list/', views.CoinList.as_view(), name='coins-list'),
]
