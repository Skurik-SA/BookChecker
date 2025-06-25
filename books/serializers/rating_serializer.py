from rest_framework import serializers

from books.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['score', 'scale']