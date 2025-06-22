from django.db import models

from books.models.genre import Genre


class Book(models.Model):
    title       = models.CharField(max_length=255)
    author      = models.CharField(max_length=255)
    total_pages = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    cover_url   = models.URLField(blank=True)
    genres      = models.ManyToManyField(Genre, related_name='books')

    def __str__(self):
        return self.title