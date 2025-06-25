from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, permissions, filters

from books.models import ReadingEntry
from books.serializers.reading_entry_serializer import ReadingEntrySerializer


@extend_schema_view(
    get=extend_schema(
        summary="Список записей чтения",
        description=(
            "Получить список записей чтения с поддержкой поиска (`?search=…` по book__title/book__author), "
            "фильтрации по статусу (`?status=…`) и сортировки (`?ordering=…` по started_at, finished_at, "
            "book__title, rating__score)."
        )
    ),
    post=extend_schema(
        summary="Создать запись чтения",
        description=(
            "Создать новую запись чтения. Доступно только для аутентифицированных пользователей. "
            "Запись будет автоматически связана с текущим пользователем."
        )
    ),
)
class ReadingEntryListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/entries/
         ?search=…         — поиск по book__title и book__author
         &status=…         — фильтр по статусу (TO_READ, READING, READ)
         &ordering=…       — сортировка по started_at, finished_at,
                             book__title, rating__score
    POST /api/entries/ — создать новую запись (только для аутентифицированных)
    """
    serializer_class = ReadingEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['status']
    search_fields    = ['book__title', 'book__author']
    ordering_fields  = [
        'added_at',
        'started_at',
        'finished_at',
        'book__title',
        'rating__score',
    ]
    ordering = ['-started_at']

    def get_queryset(self):
        return ReadingEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)