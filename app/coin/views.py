"""
Views for the Coin API.
"""
import requests
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from core.models import Coin
from .serializers import CoinSerializer


class CoinList(generics.ListCreateAPIView):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    pagination_class = PageNumberPagination

    coins = []

    def get(self, request, *args, **kwargs):
        """Download data from coingecko"""
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
        response = requests.get(url)
        coins_data = response.json()

        """Iterate through data and add it to database"""
        for coin_data in coins_data:
            coin = Coin.objects.create(
                name=coin_data['name'],
                symbol=coin_data['symbol'],
                price=coin_data['current_price'],
                market_cap=coin_data['market_cap']
                )
            coin.save()
            self.coins.append(coin)

        return self.list(request, *args, **kwargs)
