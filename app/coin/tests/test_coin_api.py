"""
Tests for coin API.
"""
import requests
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Coin

from coin.serializers import (
    CoinSerializer,
    CoinDetailSerializer,
)

COINS_URL = reverse('coin:coin-list')


def detail_url(recipe_id):
    """Create and return a coin detail URL"""
    return reverse('coin:coin-detail', args=[recipe_id])


def get_coins(user):
    """Get a list of coins from coingecko API."""
    response = requests.get('https://api.coingecko.com/api/v3/coins/markets',
                            params={'vs_currency': 'usd',
                                    'sparkline': 'false',
                                    'price_change_percentage': '24h'})
    data = response.json()

    # aktualizuj dane monet w bazie danych
    for x in data:
        coin, created = Coin.objects.get_or_create(coin_id=x['id'])
        coin.name = x['name']
        coin.symbol = x['symbol']
        coin.price = x['current_price']
        coin.price_change_percentage = x['price_change_percentage_24h']
        coin.save()

    # zwróć listę aktualnych danych o monetach z bazy danych
    queryset = Coin.objects.all()
    return queryset.order_by('id')


class PublicCoinAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(COINS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCoinAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieving_coins(self):
        """Test retrieving a list of coins"""
        get_coins(user=self.user)

        res = self.client.get(COINS_URL)

        coins = Coin.objects.all().order_by('id')
        serializer = CoinSerializer(coins, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_get_recipe_detail(self):
    #     """Test get recipe detail"""
    #     coin = self.coin
    #     print(coin)
    #
    #     url = detail_url(coin.id)
    #     res = self.client.get(url)
    #
    #     serializer = CoinDetailSerializer(coin)
    #     self.assertEqual(res.data, serializer.data)
