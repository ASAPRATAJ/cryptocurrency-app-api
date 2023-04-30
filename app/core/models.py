"""
Database models.
"""
import requests

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create. save and return a new user."""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    gem_finder = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class CoinManager(models.Manager):
    def get_list_of_coins(self):
        response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd')
        coin_data = response.json()
        coins = []
        for coin in coin_data:
            coin_obj, created = Coin.objects.get_or_create(
                coin_id=coin['id'],
                defaults={
                    'name': coin['name'],
                    'symbol': coin['symbol'],
                    'price': coin['current_price'],
                }
            )
            if not created:
                coin_obj.name = coin['name']
                coin_obj.symbol = coin['symbol']
                coin_obj.price = coin['current_price']
                coin_obj.save()
            coins.append(coin_obj)
        return coins


class Coin(models.Model):
    """Coin object."""
    coin_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    price = models.FloatField(default=0)

    objects = CoinManager()

    def __str__(self):
        return self.coin_id
