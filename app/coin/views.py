"""
Views for the coin APIs.
"""
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from core.models import Coin
from coin import serializers


class CoinListView(APIView):
    """View for retrieving a list of coins."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        coins = Coin.objects.get_list_of_coins()
        serializer = serializers.CoinSerializer(coins, many=True)
        return Response(serializer.data)
