"""
Serializers for the Coin API.
"""


from rest_framework import serializers
from core.models import Coin


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'
