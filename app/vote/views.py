"""Views for the vote APIs."""
from datetime import datetime

from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from core.models import Vote

from vote import serializers


class VoteViewSet(viewsets.ModelViewSet):
    """View for manage vote APIs."""
    serializer_class = serializers.VoteDetailSerializer
    queryset = Vote.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.VoteSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create new vote and update number of User votes_left."""
        user = self.request.user
        date = datetime.now()
        if date.day != 1:
            raise ValidationError(
                "You can only vote on the first day of the month."
            )

        if user.votes_left <= 0:
            raise ValidationError("You have already used all your votes.")

        coin = serializer.validated_data['coin']
        existing_vote = Vote.objects.filter(
            user=user,
            coin=coin
        ).first()

        if existing_vote:
            raise ValidationError(
                "You have already voted for this coin. "
                "Please vote on another coin."
            )

        price = coin.price

        serializer.save(user=user, price=price)
        user.votes_left -= 1
        user.save()

    def destroy(self, request, *args, **kwargs):
        """Disable the delete operation for normal user."""
        if not request.user.is_superuser:
            raise PermissionDenied(
                "You do not have permission to perform this action."
            )

        return super().partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Update vote data partially denied for normal user."""
        if not request.user.is_superuser:
            raise PermissionDenied(
                "You do not have permission to perform this action."
            )

        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Update vote data denied for normal user."""
        if not request.user.is_superuser:
            raise PermissionDenied(
                "You do not have permission to perform this action."
            )

        return super().partial_update(request, *args, **kwargs)
