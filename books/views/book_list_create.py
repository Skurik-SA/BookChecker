from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, permissions, filters

from books.models import Book
from books.serializers.book_serializer import BookSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Список книг",
        description=(
            "Получить список книг с поддержкой поиска (`?search=…` по title/author) "
            "и сортировки (`?ordering=…` по title, author, total_pages)."
        )
    ),
    post=extend_schema(
        summary="Добавить книгу",
        description="Создать новую книгу (доступно только авторизованным пользователям)."
    ),
)
class BookListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/books/?search=…&ordering=…   — поиск по title/author и сортировка\n
    POST /api/books/                       — добавить новую книгу (только для аутентифицированных)
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'author', 'total_pages']
    ordering = ['title']  # сортировка по-умолчанию


    def get_queryset(self):
        qs = Book.objects.all()
        user = self.request.user

        if user.is_authenticated:
            qs = qs.annotate_user_status(user)
        return qs

    def perform_create(self, serializer):
        # любой авторизованный пользователь может добавлять
        serializer.save()