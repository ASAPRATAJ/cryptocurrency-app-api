"""
URL mapping for the coin app.
"""
from django.urls import path

from coin.views import CoinListView

app_name = 'coin'

urlpatterns = [
    path('list/', CoinListView.as_view(), name='coin-list'),
]
