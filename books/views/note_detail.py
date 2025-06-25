from django.core.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, permissions

from books.models import ReadingEntry
from books.permissions import IsOwner
from books.serializers.note_serializer import NoteSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Получить заметку",
        description=(
            "Получить заметку по ID. Доступно только владельцу записи чтения. "
            "Если заметка не найдена, будет возвращена ошибка 404."
        )
    ),
    put=extend_schema(
        summary="Обновить заметку",
        description=(
            "Обновить заметку по ID. Доступно только владельцу записи чтения. "
            "Если заметка не найдена, будет возвращена ошибка 404."
        )
    ),
    delete=extend_schema(
        summary="Удалить заметку",
        description=(
            "Удалить заметку по ID. Доступно только владельцу записи чтения. "
            "Если заметка не найдена, будет возвращена ошибка 404."
        )
    ),
)
class NoteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/entries/{entry_id}/notes/{note_id}/
    PUT    /api/entries/{entry_id}/notes/{note_id}/
    DELETE /api/entries/{entry_id}/notes/{note_id}/
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_url_kwarg = 'note_id'

    def get_queryset(self):
        entry = ReadingEntry.objects.get(pk=self.kwargs['entry_id'])
        if entry.user != self.request.user:
            raise PermissionDenied()
        return entry.notes.all()