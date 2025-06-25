from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, permissions

from books.models.statistic import Statistics
from books.serializers.statistic_serializer import StatisticsSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Получить статистику",
        description=(
            "Получить статистику по текущему пользователю. "
            "Если статистика не найдена, будет создана новая запись с нулевыми значениями."
        )
    ),
)
class StatisticsRetrieveAPIView(generics.RetrieveAPIView):
    """
    GET /api/statistics/ — возвращает статистику по текущему пользователю
    """
    serializer_class = StatisticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Получаем или создаём при первом запуске
        stats, _ = Statistics.objects.get_or_create(user=self.request.user)
        return stats