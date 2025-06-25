from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, permissions

from books.models import ReadingEntry
from books.permissions import IsOwner
from books.serializers.reading_entry_serializer import ReadingEntrySerializer


@extend_schema_view(
    get=extend_schema(
        summary="Получить запись",
        description=(
            "Получить запись чтения по ID. "
            "Доступно только владельцу записи чтения. "
            "Если запись не найдена, будет возвращена ошибка 404."
        )
    ),
    put=extend_schema(
        summary="Обновить запись",
        description=(
            "Обновить запись чтения по ID. "
            "Доступно только владельцу записи чтения. "
            "Если запись не найдена, будет возвращена ошибка 404."
        )
    ),
    delete=extend_schema(
        summary="Удалить запись",
        description=(
            "Удалить запись чтения по ID. "
            "Доступно только владельцу записи чтения. "
            "Если запись не найдена, будет возвращена ошибка 404."
        )
    ),
)
class ReadingEntryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/entries/{id}/  — получить одну запись
    PUT    /api/entries/{id}/  — обновить запись (включая статус/даты)
    DELETE /api/entries/{id}/  — удалить запись (только владелец)
    """
    serializer_class = ReadingEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_url_kwarg = 'entry_id'

    def get_queryset(self):
        return ReadingEntry.objects.filter(user=self.request.user)