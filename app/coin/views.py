"""
Views for the coin APIs.
"""
from rest_framework.views import APIView
from rest_framework.response import Response

from coin.serializers import (
    CoinSerializer,
    CoinDetailSerializer
)
from coin import common


class CoinView(APIView):
    serializer_class = CoinDetailSerializer

    def get(self, *args):
        """Fetch coin data from coingecko"""
        queryset = common.fetch_coin_data()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self, method):
        """Return the serializer class based on the request method."""
        if method == 'GET':
            return CoinSerializer
        return self.serializer_class
