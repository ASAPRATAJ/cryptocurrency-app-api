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
        read_only_fields = ['id']


class CoinDetailSerializer(CoinSerializer):
    """Serializer for coin details."""

    class Meta(CoinSerializer.Meta):
        fields = CoinSerializer.Meta.fields + ['price_change_percentage']
