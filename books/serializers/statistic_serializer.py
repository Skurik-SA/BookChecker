from rest_framework import serializers

from books.models.statistic import Statistics
from books.serializers.genre_serializer import GenreSerializer


class StatisticsSerializer(serializers.ModelSerializer):
    favorite_genre = GenreSerializer(read_only=True)
    monthly_graph  = serializers.JSONField(read_only=True)
    yearly_graph   = serializers.JSONField(read_only=True)

    class Meta:
        model = Statistics
        fields = [
            'total_books',
            'total_pages',
            'favorite_genre',
            'monthly_graph',
            'yearly_graph',
            'updated_at',
        ]
        read_only_fields = fields