from django.db import models
from books.models.genre import Genre
from django.core.validators import FileExtensionValidator
from django.db.models import Case, When, Value, CharField

class BookQuerySet(models.QuerySet):
    def annotate_user_status(self, user):
        if user.is_anonymous:
            return self

        return self.annotate(
            user_status=Case(
                When(reading_entries__user=user, then='reading_entries__status'),
                default=Value(None),
                output_field=CharField()
            )
        )


class Book(models.Model):
    objects = BookQuerySet.as_manager()

    title       = models.CharField(max_length=255)
    author      = models.CharField(max_length=255)
    total_pages = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    cover        = models.ImageField(
        upload_to='book_covers/%Y/%m/%d/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    genres      = models.ManyToManyField(Genre, related_name='books')

    def __str__(self):
        return self.title