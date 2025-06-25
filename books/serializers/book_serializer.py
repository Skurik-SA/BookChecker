from rest_framework import serializers

from books.models import Book, Genre


class BookSerializer(serializers.ModelSerializer):
    genres = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
        write_only=True
    )
    genre_names = serializers.SerializerMethodField(read_only=True)
    cover = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model  = Book
        fields = ['id', 'title', 'author', 'total_pages', 'description', 'cover', 'genres', 'genre_names']

    def create(self, validated_data):
        genre_names = validated_data.pop('genres', [])
        book = Book.objects.create(**validated_data)
        self._handle_genres(book, genre_names)

        return book

    def update(self, instance, validated_data):
        genre_names = validated_data.pop('genres', None)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)

        instance.save()

        if genre_names is not None:
            instance.genres.clear()
            self._handle_genres(instance, genre_names)

        return instance

    def get_genre_names(self, obj):
        return [g.name for g in obj.genres.all()]

    def _handle_genres(self, book, genre_names):
        """
        Для каждого имени жанра:
        — если есть Genre с таким name (игнорируя регистр) — привязываем его;
        — иначе создаём новый Genre(is_custom=True, created_by=user).
        """
        user = self.context['request'].user
        for name in genre_names:
            name = name.strip()
            if not name:
                continue
            genre, created = Genre.objects.get_or_create(
                name__iexact=name,
                defaults={
                    'name': name,
                    'is_custom': True,
                    'created_by': user if user.is_authenticated else None
                }
            )
            book.genres.add(genre)