"""
Serializers for vote APIs.
"""
from rest_framework import serializers

from core.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    """Serializer for votes."""

    class Meta:
        model = Vote
        fields = ['id', 'user', 'coin']
        read_only_fields = ['id']


class VoteDetailSerializer(VoteSerializer):
    """Serializer for vote detail view."""

    class Meta(VoteSerializer.Meta):
        fields = VoteSerializer.Meta.fields + ['reason']
