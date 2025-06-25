from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, permissions

from books.models import Book
from books.serializers.book_serializer import BookSerializer


@extend_schema_view(
    delete=extend_schema(
        summary="Удалить книгу",
        description=(
            "Удалить книгу по ID. Доступно только администраторам. "
            "Если книга не найдена, будет возвращена ошибка 404."
            "Удаление книги не влияет на записи чтения, связанные с ней."
        )
    ),
)
class BookDestroyAPIView(generics.DestroyAPIView):
    """
    DELETE /api/books/{pk}/ — удалить книгу (только админ)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]