"""
Tests for coin API.
"""
import requests
from coin import common
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


def detail_url(coin_id):
    """Create and return a coin detail URL"""
    return reverse('coin:coin-detail', args=[coin_id])


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
            email='user@example.com',
            password='test123'
        )
        self.client.force_authenticate(self.user)

        self.coin = Coin.objects.create(
            coin_id='coin1',
            name='Coin 1',
            symbol='C1',
            price=10.0
        )

    def test_retrieving_coins(self):
        """Test retrieving a list of coins"""
        coins = common.fetch_coin_data()

        res = self.client.get(COINS_URL)

        serializer = CoinSerializer(coins, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_coin_detail(self):
        """Test retrieve coin details."""
        coins = common.fetch_coin_data()

        for coin in coins:
            coin_id = coin.id
            url = detail_url(coin_id)
            res = self.client.get(url)
            serializer = CoinDetailSerializer(coin)
            self.assertEqual(res.data, serializer.data)

    def test_delete_coin_denied(self):
        """Test deleting a coin is denied."""
        coins = common.fetch_coin_data()

        for coin in coins:
            coin_id = coin.id
            url = detail_url(coin_id)
            res = self.client.delete(url)

            self.assertEqual(
                res.status_code,
                status.HTTP_405_METHOD_NOT_ALLOWED
            )
            self.assertTrue(Coin.objects.filter(id=coin.id).exists())

    def test_partial_update_coin_by_user_returns_error(self):
        """Test changing the coin price by user results in an error."""
        url = detail_url(self.coin.id)
        payload = {'price': 20.0}

        res = self.client.patch(url, payload)

        self.coin.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.coin.price, payload['price'])

    def test_full_update_coin_by_user_returns_error(self):
        """Test changing the coin details by user results in an error."""
        url = detail_url(self.coin.id)
        payload = {
            'coin_id': 'NewTestID',
            'name': 'NewTestName',
            'symbol': 'NTS',
            'price': 100.0,
        }
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.coin.refresh_from_db()

        self.assertNotEqual(self.coin.coin_id, payload['coin_id'])
