from django.core.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, permissions

from books.models import ReadingEntry
from books.permissions import IsOwner
from books.serializers.note_serializer import NoteSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Список заметок",
        description=(
            "Получить список заметок по записи чтения. "
            "Доступно только владельцу записи чтения. "
            "Если запись не найдена, будет возвращена ошибка 404."
        )
    ),
    post=extend_schema(
        summary="Создать заметку",
        description=(
            "Создать новую заметку для записи чтения. "
            "Доступно только владельцу записи чтения. "
            "Если запись не найдена, будет возвращена ошибка 404."
        )
    ),
)
class NoteListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/entries/{entry_id}/notes/   — список заметок по записи
    POST /api/entries/{entry_id}/notes/   — создать заметку (только владелец entry)
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        entry = ReadingEntry.objects.get(pk=self.kwargs['entry_id'])
        if entry.user != self.request.user:
            raise PermissionDenied()
        return entry.notes.all()

    def perform_create(self, serializer):
        entry = ReadingEntry.objects.get(pk=self.kwargs['entry_id'])
        if entry.user != self.request.user:
            raise PermissionDenied()
        serializer.save(entry=entry)