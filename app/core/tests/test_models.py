"""
Tests for models.
"""
from datetime import datetime

import requests
from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

import coin.apps
from core import models


# def retrieve_from_api(coin):
#     """Fetch coins from coingecko API."""
#     response = requests.get('https://api.coingecko.com/api/v3/coins/markets',
#                             params={'vs_currency': 'usd'})
#     data = response.json()
#     coins = []
#     for coin_data in data:
#         coin, created = coin().objects.get_or_create(coingecko_id=coin_data['id'])
#         coin.name = coin_data['name']
#         coin.symbol = coin_data['symbol']
#         coin.price = coin_data['current_price']
#         coin.save()
#         coins.append(coin_data)
#     return coins


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
            ['test5@example.Com', 'test5@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'testpass123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'testpass123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_coin(self):
        """Test creating a coin is successful."""
        coin = models.Coin.objects.create(
            coin_id='testcoin',
            name='Testcoin',
            symbol='TST',
            price=100,
            price_change_percentage=14.2,
        )
        self.assertEqual(str(coin), coin.coin_id)

    def test_create_vote(self):
        """Test creating a vote is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        coin = models.Coin.objects.create(
            coin_id='testcoin',
            name='Testcoin',
            symbol='TST',
            price=100,
            price_change_percentage=14.2,
        )

        vote = models.Vote.objects.create(
            user=user,
            coin=coin,
            price=coin.price,
            reason='Test reason',
        )
        self.assertEqual(str(coin), coin.coin_id)
        self.assertEqual(str(vote), f'{vote.user} - {vote.coin} - {vote.created_at}')
        self.assertEqual(vote.user, user)
        self.assertEqual(vote.coin, coin)
        self.assertEqual(vote.reason, 'Test reason')
        self.assertTrue(models.Vote.objects.exists())
