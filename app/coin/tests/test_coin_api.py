"""
Tests for coin API.
"""
import requests

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Coin, CoinManager

from coin.serializers import (
    CoinSerializer,
)

COINS_URL = reverse('coin:coin-list')


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

    def test_retrieve_coins(self):
        """Test retrieving a list of coins."""
        coin = CoinManager()
        coin.get_list_of_coins()

        res = self.client.get(COINS_URL)

        coins = Coin.objects.all()
        serializer = CoinSerializer(coins, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        