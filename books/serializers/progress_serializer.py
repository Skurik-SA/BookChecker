from rest_framework import serializers

from books.models import Progress


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['current_page', 'percent', 'updated_at']
        read_only_fields = ['percent', 'updated_at']
