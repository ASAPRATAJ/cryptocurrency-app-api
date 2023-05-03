from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Vote, Coin

from vote import serializers


class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VoteDetailSerializer
    queryset = Vote.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.VoteSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new vote."""
        user = self.request.user
        if user.votes_left <= 0:
            raise ValidationError("You have already used all your votes.")

        coin = serializer.validated_data['coin']
        existing_vote = Vote.objects.filter(user=user, coin=coin).first()
        if existing_vote:
            raise ValidationError("You have already voted for this coin.")

        serializer.save(user=user)
        user.votes_left -= 1
        user.save()