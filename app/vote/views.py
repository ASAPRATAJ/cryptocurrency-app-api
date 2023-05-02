from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Vote

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
        serializer.save(user=self.request.user)
