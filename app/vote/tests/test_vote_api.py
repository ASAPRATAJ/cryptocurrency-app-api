"""Tests for the vote API."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Vote, Coin

from vote.serializers import (
    VoteSerializer,
    VoteDetailSerializer,
)

VOTES_URL = reverse('vote:vote-list')


def detail_url(vote_id):
    """Create and return a vote detail URL"""
    return reverse('vote:vote-detail', args=[vote_id])


def create_vote(user, coin):
    """Create and return a sample vote."""
    vote = Vote.objects.create(
        user=user,
        coin=coin,
        price=coin.price,
        reason='Test reason',
    )
    return vote


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(VOTES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test authenticated API request."""

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
        self.coin_two = Coin.objects.create(
            coin_id='coin2',
            name='Coin 2',
            symbol='C2',
            price=20.0
        )

    def test_retrieve_votes(self):
        """Test retrieving a list of votes"""

        create_vote(user=self.user, coin=self.coin)
        create_vote(user=self.user, coin=self.coin_two)

        res = self.client.get(VOTES_URL)

        votes = Vote.objects.all().order_by('-id')
        serializer = VoteSerializer(votes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertCountEqual(res.data, serializer.data)

    def test_get_vote_detail(self):
        """Test get vote detail"""
        vote = create_vote(user=self.user, coin=self.coin)

        url = detail_url(vote.id)
        res = self.client.get(url)

        serializer = VoteDetailSerializer(vote)
        self.assertEqual(res.data, serializer.data)

    def test_create_vote(self):
        """Test creating a vote"""
        payload = {
            'user': self.user.id,
            'coin': self.coin.id,
            'price': self.coin.price,
            'reason': 'Test reason'
        }

        res = self.client.post(VOTES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        vote = Vote.objects.get(id=res.data['id'])
        self.assertEqual(vote.user, self.user)
        self.assertEqual(vote.coin, self.coin)

    def test_delete_vote_denied(self):
        """Test deleting a recipe is denied."""
        vote = create_vote(user=self.user, coin=self.coin)

        url = detail_url(vote.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Vote.objects.filter(id=vote.id).exists())

    def test_partial_update_vote_by_user_returns_error(self):
        """Test changing vote detail by user results in an error."""
        vote = create_vote(user=self.user, coin=self.coin)
        url = detail_url(vote.id)

        payload = {'price': 20.0}

        res = self.client.patch(url, payload)

        self.coin.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(vote.price, payload['price'])

    def test_full_update_vote_by_user_returns_error(self):
        """Test changing the coin details by user results in an error."""
        vote = create_vote(user=self.user, coin=self.coin)
        url = detail_url(vote.id)
        new_user = get_user_model().objects.create_user(
            email='newuser@example.com',
            password='testpass123'
        )
        payload = {
            'user': new_user,
            'coin': self.coin_two,
            'price': self.coin_two.price,
            'reason': 'New reason',
        }
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.coin.refresh_from_db()

        self.assertNotEqual(vote.user, payload['user'])
        self.assertNotEqual(vote.coin, payload['coin'])
        self.assertNotEqual(vote.price, payload['price'])
        self.assertNotEqual(vote.reason, payload['reason'])
