"""
Database models.
"""
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
    votes_left = models.IntegerField(default=3)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Coin(models.Model):
    """Coin object."""
    coin_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    price = models.FloatField(default=0)
    price_change_percentage = models.DecimalField(null=True, default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.coin_id


class Vote(models.Model):
    """Vote object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.coin} - {self.created_at}'
