"""
Views for the coin APIs.
"""
import requests
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from coin import common
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Coin

from coin.serializers import (
    CoinSerializer,
    CoinDetailSerializer
)


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

# class CoinViewSet(viewsets.ModelViewSet):
#     """View for retrieving a list of coins."""
#     serializer_class = CoinDetailSerializer
#     queryset = Coin.objects.all()
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def list(self, request, *args, **kwargs):
#         """Get coin data from CoinGecko API."""
#         queryset = common.fetch_coin_data()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def get_serializer_class(self):
#         """Return the serializer class for request."""
#         if self.action == 'list':
#             return CoinSerializer
#
#         return self.serializer_class
#
#     def destroy(self, request, *args, **kwargs):
#         """Disable the delete operation."""
#         raise MethodNotAllowed(request.method)
#
#     def partial_update(self, request, *args, **kwargs):
#         """Update coin data partially denied for normal user."""
#         if not request.user.is_superuser:
#             raise PermissionDenied(
#                 "You do not have permission to perform this action."
#             )
#
#         return super().partial_update(request, *args, **kwargs)
#
#     def update(self, request, *args, **kwargs):
#         """Update coin data denied for normal user."""
#         if not request.user.is_superuser:
#             raise PermissionDenied(
#                 "You do not have permission to perform this action."
#             )
#
#         return super().partial_update(request, *args, **kwargs)
