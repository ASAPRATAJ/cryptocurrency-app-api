"""
Views for the coin APIs.
"""
import requests
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Coin
from coin import serializers


class CoinViewSet(viewsets.ModelViewSet):
    """View for retrieving a list of coins."""
    serializer_class = serializers.CoinDetailSerializer
    queryset = Coin.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """Get coin data from CoinGecko API."""
        response = requests.get('https://api.coingecko.com/api/v3/coins/markets',
                                params={'vs_currency': 'usd',
                                        'sparkline': 'false',
                                        'price_change_percentage': '30d'})
        data = response.json()

        for coin in data:
            coin_data = {
                'coin_id': coin['id'],
                'name': coin['name'],
                'symbol': coin['symbol'],
                'price': coin['current_price'],
                'price_change_percentage': coin.get('price_change_percentage_30d_in_currency')
            }
            Coin.objects.update_or_create(coin_id=coin['id'], defaults=coin_data)

        queryset = Coin.objects.all().order_by('id')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.CoinSerializer

        return self.serializer_class

    def destroy(self, request, *args, **kwargs):
        """Disable the delete operation."""
        raise MethodNotAllowed(request.method)

    def partial_update(self, request, *args, **kwargs):
        """Update coin data partially denied for normal user."""
        if not request.user.is_superuser:
            raise PermissionDenied(
                "You do not have permission to perform this action."
            )

        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Update coin data denied for normal user."""
        if not request.user.is_superuser:
            raise PermissionDenied(
                "You do not have permission to perform this action."
            )

        return super().partial_update(request, *args, **kwargs)
