"""
URL mapping for the coin app.
"""
from django.urls import path

from coin import views

app_name = 'coin'

urlpatterns = [
    path('list/', views.CoinView.as_view(), name='list')
]
