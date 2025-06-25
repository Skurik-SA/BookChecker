from django.db import transaction
from rest_framework import serializers

from books.models import Book, ReadingEntry, Progress, Rating
from books.serializers.book_serializer import BookSerializer
from books.serializers.note_serializer import NoteSerializer
from books.serializers.progress_serializer import ProgressSerializer
from books.serializers.rating_serializer import RatingSerializer

# STATUS_CHOICES = [
#     ('TO_READ', 'Хочу читать'),
#     ('READING', 'Читаю сейчас'),
#     ('READ', 'Прочитано'),
# ]


class ReadingEntrySerializer(serializers.ModelSerializer):
    # Позволяем либо передавать существующую книгу по ID, либо создавать новую
    book = BookSerializer(required=False)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source='book',
        write_only=True,
        required=False
    )

    progress = ProgressSerializer(required=False)
    rating = RatingSerializer(required=False)
    # notes = NoteSerializer(many=True, read_only=True)
    notes = serializers.SerializerMethodField()

    class Meta:
        model = ReadingEntry
        fields = [
            'id', 'book', 'book_id',
            'status', 'started_at', 'finished_at', 'added_at',
            'progress', 'rating', 'notes'
        ]
        read_only_fields = ['id', 'notes', 'added_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance is not None:
            self.fields['status'].required = False

    def get_notes(self, instance):
        # просто список, можно и nested NoteSerializer(many=True, read_only=True)
        return NoteSerializer(instance.notes.all(), many=True).data

    def validate(self, attrs):
        # Обязательность только при создании
        if self.instance is None and 'book' not in attrs:
            raise serializers.ValidationError(
                "При создании нужно передать либо book_id, либо nested book."
            )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user

        # 1) Вытаскиваем всё, что передали в validated_data под ключом 'book'
        book_field = validated_data.pop('book')

        # 2) Разбираем, что там — dict (nested) или уже Book
        if isinstance(book_field, dict):
            # создаём новую книгу
            book_serializer = BookSerializer(
                data=book_field,
                context=self.context
            )
            book_serializer.is_valid(raise_exception=True)
            book = book_serializer.save()
        else:
            # это уже Book instance из book_id
            book = book_field

        # Вытаскиваем прогресс и рейтинг, если передали
        progress_data = validated_data.pop('progress', None)
        rating_data   = validated_data.pop('rating',   None)

        # 3) Создаём запись о чтении
        entry = ReadingEntry.objects.create(
            user=user,
            book=book,
            status=validated_data.get('status'),
            started_at=validated_data.get('started_at'),
            finished_at=validated_data.get('finished_at'),
        )

        # 3) Создаём/апдейтим Progress
        prog = Progress.objects.create(entry=entry)
        if progress_data and 'current_page' in progress_data:
            prog.current_page = progress_data['current_page']
            prog.save()  # percent пересчитается в модели

        # 4) Создаём/апдейтим Rating
        rat = Rating.objects.create(entry=entry, score=0)
        if rating_data:
            for attr, val in rating_data.items():
                setattr(rat, attr, val)
            rat.save()

        # # 6) Дефолтные связанные объекты
        # Progress.objects.create(entry=entry)
        # Rating.objects.create(entry=entry, score=0)

        return entry

    @transaction.atomic
    def update(self, instance, validated_data):
        # 1) обновляем только статус и даты
        for attr in ('status', 'started_at', 'finished_at'):
            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])
        instance.save()

        # 2) Обновляем Progress, если есть в запросе
        prog_data = validated_data.get('progress')
        if prog_data and 'current_page' in prog_data:
            prog = instance.progress
            prog.current_page = prog_data['current_page']
            prog.save()   # percent пересчитается в модели

        # 3) Обновляем Rating, если есть
        rat_data = validated_data.get('rating')
        if rat_data:
            rat = instance.rating
            for attr, val in rat_data.items():
                setattr(rat, attr, val)
            rat.save()

        return instance