"""
Serializers for coin APIs.
"""
from rest_framework import serializers

from core.models import Coin


class CoinSerializer(serializers.ModelSerializer):
    """Serializer for coins."""

    class Meta:
        model = Coin
        fields = ['id', 'coin_id', 'name', 'symbol', 'price']
        read_only_fields = ['id', 'price']
