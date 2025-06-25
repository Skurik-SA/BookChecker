from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, permissions

from books.models import Book
from books.serializers.book_serializer import BookSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Получить одну книгу",
        description=(
            "Получить данные книги по её ID. "
            "Если пользователь аутентифицирован, то также будет возвращён статус книги "
            "(например, прочитана/в процессе/не начинал и т.д.)."
        )
    ),
)
class BookDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/books/{pk}/   — получить данные книги
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Book.objects.all()
        user = self.request.user

        if user.is_authenticated:
            qs = qs.annotate_user_status(user)
        return qs
