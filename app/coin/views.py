"""
Views for the coin APIs.
"""
import requests
from django.http import JsonResponse
from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Coin
from coin import serializers


class CoinViewSet(viewsets.ModelViewSet):
    """View for retrieving a list of coins."""
    serializer_class = serializers.CoinSerializer
    queryset = Coin.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # pobierz aktualną listę monet z CoinGecko API
        response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd')
        data = response.json()

        # aktualizuj dane monet w bazie danych
        for x in data:
            coin, created = Coin.objects.get_or_create(coin_id=x['id'])
            coin.name = x['name']
            coin.symbol = x['symbol']
            coin.price = x['current_price']
            coin.save()

        # zwróć listę aktualnych danych o monetach z bazy danych
        queryset = Coin.objects.all()
        return queryset.order_by('id')
